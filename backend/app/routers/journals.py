from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models import Journal
from app.services.nlm_catalog import search_nlm_journals

router = APIRouter()


class JournalOut(BaseModel):
    id: int
    name: str
    issn: Optional[str]
    iso_abbreviation: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True


class PubmedJournalOut(BaseModel):
    """Journal from PubMed/NLM Catalog (no local DB id)."""
    name: str
    issn: Optional[str]
    iso_abbreviation: Optional[str]
    nlm_id: Optional[str]
    is_local: bool = False  # Whether it exists in our DB


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


@router.get("/pubmed-search", response_model=List[PubmedJournalOut])
async def search_pubmed_journals(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
):
    """Search journals from PubMed/NLM Catalog."""
    # First get local matches to mark them
    local_result = await db.execute(
        select(Journal).where(Journal.name.ilike(f"%{q}%")).limit(50)
    )
    local_journals = {j.issn: j for j in local_result.scalars().all() if j.issn}
    
    # Search NLM Catalog
    nlm_journals = await search_nlm_journals(q, limit=20)
    
    results = []
    for j in nlm_journals:
        is_local = j.issn in local_journals if j.issn else False
        results.append(PubmedJournalOut(
            name=j.name,
            issn=j.issn,
            iso_abbreviation=j.iso_abbreviation,
            nlm_id=j.nlm_id,
            is_local=is_local,
        ))
    
    return results


@router.get("/presets/{category}", response_model=List[JournalOut])
async def get_preset_journals(
    category: str,
    db: AsyncSession = Depends(get_db),
):
    """Get preset journals by category (e.g., 'cardiology', 'medicine')."""
    result = await db.execute(
        select(Journal).where(func.lower(Journal.category) == category.lower()).limit(50)
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

