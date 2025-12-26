from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, timedelta

from app.database import get_db
from app.models import Profile, User
from app.routers.auth import get_current_user
from app.services.pubmed import fetch_articles_for_journals

router = APIRouter()


class ArticleOut(BaseModel):
    pmid: str
    title: str
    authors: List[str]
    journal: str
    pub_date: str
    abstract: Optional[str]
    doi: Optional[str]
    pubmed_url: str


@router.get("/generate", response_model=List[ArticleOut])
async def generate_brief(
    profile_id: int,
    days: int = Query(default=7, ge=1, le=90),
    from_date: Optional[str] = Query(default=None, description="Start date in YYYY-MM-DD format"),
    to_date: Optional[str] = Query(default=None, description="End date in YYYY-MM-DD format"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a brief for the given profile. Uses from_date/to_date if provided, otherwise last N days."""
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.journals))
        .where(Profile.id == profile_id, Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if not profile.journals:
        return []

    issns = [j.issn for j in profile.journals if j.issn]
    
    # Use explicit dates if provided, otherwise calculate from days
    if from_date and to_date:
        try:
            start_date = date.fromisoformat(from_date)
            end_date = date.fromisoformat(to_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        start_date = date.today() - timedelta(days=days)
        end_date = date.today()

    articles = await fetch_articles_for_journals(issns, start_date, end_date)
    return articles

