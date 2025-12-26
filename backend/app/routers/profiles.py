from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models import Profile, Journal, User
from app.routers.auth import get_current_user

router = APIRouter()


class ProfileCreate(BaseModel):
    name: str
    journal_ids: List[int]


class ProfileOut(BaseModel):
    id: int
    name: str
    journal_ids: List[int]

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProfileOut])
async def list_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.journals))
        .where(Profile.user_id == current_user.id)
    )
    profiles = result.scalars().all()
    return [
        ProfileOut(id=p.id, name=p.name, journal_ids=[j.id for j in p.journals])
        for p in profiles
    ]


@router.post("/", response_model=ProfileOut)
async def create_profile(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Fetch journals
    result = await db.execute(select(Journal).where(Journal.id.in_(data.journal_ids)))
    journals = result.scalars().all()

    profile = Profile(name=data.name, user_id=current_user.id, journals=journals)
    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return ProfileOut(id=profile.id, name=profile.name, journal_ids=[j.id for j in journals])


@router.put("/{profile_id}", response_model=ProfileOut)
async def update_profile(
    profile_id: int,
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a profile's name and journals."""
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.journals))
        .where(Profile.id == profile_id, Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Fetch new journals
    journal_result = await db.execute(select(Journal).where(Journal.id.in_(data.journal_ids)))
    journals = journal_result.scalars().all()

    profile.name = data.name
    profile.journals = journals
    await db.commit()
    await db.refresh(profile)

    return ProfileOut(id=profile.id, name=profile.name, journal_ids=[j.id for j in profile.journals])


@router.delete("/{profile_id}")
async def delete_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a profile."""
    result = await db.execute(
        select(Profile).where(Profile.id == profile_id, Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    await db.delete(profile)
    await db.commit()
    return {"message": "Profile deleted"}

