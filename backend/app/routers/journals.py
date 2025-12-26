from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models import Journal

router = APIRouter()


class JournalOut(BaseModel):
    id: int
    name: str
    issn: Optional[str]
    iso_abbreviation: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True


@router.get("/search", response_model=List[JournalOut])
async def search_journals(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
):
    """Search journals by name (case-insensitive partial match)."""
    result = await db.execute(
        select(Journal).where(Journal.name.ilike(f"%{q}%")).limit(20)
    )
    return result.scalars().all()


@router.get("/presets/{category}", response_model=List[JournalOut])
async def get_preset_journals(
    category: str,
    db: AsyncSession = Depends(get_db),
):
    """Get preset journals by category (e.g., 'cardiology', 'medicine')."""
    result = await db.execute(
        select(Journal).where(Journal.category.ilike(category)).limit(10)
    )
    return result.scalars().all()


@router.get("/by-ids", response_model=List[JournalOut])
async def get_journals_by_ids(
    ids: str = Query(..., description="Comma-separated list of journal IDs"),
    db: AsyncSession = Depends(get_db),
):
    """Get journals by IDs."""
    try:
        id_list = [int(x.strip()) for x in ids.split(",") if x.strip()]
    except ValueError:
        return []
    
    if not id_list:
        return []
    
    result = await db.execute(
        select(Journal).where(Journal.id.in_(id_list))
    )
    return result.scalars().all()

