from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models import Profile, Journal, User
from app.routers.auth import get_current_user

router = APIRouter()


class NewJournal(BaseModel):
    """New journal from PubMed to be added to DB."""
    name: str
    issn: Optional[str] = None
    iso_abbreviation: Optional[str] = None


class ProfileCreate(BaseModel):
    name: str
    journal_ids: List[int] = []
    new_journals: List[NewJournal] = []


class ProfileOut(BaseModel):
    id: int
    name: str
    journal_ids: List[int]
    is_default: bool = False

    class Config:
        from_attributes = True


class SetDefaultRequest(BaseModel):
    is_default: bool = True


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
        ProfileOut(id=p.id, name=p.name, journal_ids=[j.id for j in p.journals], is_default=p.is_default)
        for p in profiles
    ]


@router.post("/", response_model=ProfileOut)
async def create_profile(
    data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    journals = []
    
    # Fetch existing journals by ID
    if data.journal_ids:
        result = await db.execute(select(Journal).where(Journal.id.in_(data.journal_ids)))
        journals.extend(result.scalars().all())
    
    # Create new journals from PubMed (if they don't exist)
    for new_j in data.new_journals:
        # Check if journal with same ISSN already exists
        existing = None
        if new_j.issn:
            result = await db.execute(select(Journal).where(Journal.issn == new_j.issn))
            existing = result.scalar_one_or_none()
        
        if existing:
            journals.append(existing)
        else:
            # Create new journal
            journal = Journal(
                name=new_j.name,
                issn=new_j.issn,
                iso_abbreviation=new_j.iso_abbreviation,
                category="Custom",  # Mark as custom/user-added
            )
            db.add(journal)
            await db.flush()  # Get the ID
            journals.append(journal)

    # Check if this is the user's first profile
    result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
    existing_profiles = result.scalars().all()
    is_first_profile = len(existing_profiles) == 0

    profile = Profile(
        name=data.name,
        user_id=current_user.id,
        journals=journals,
        is_default=is_first_profile  # First profile is automatically default
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)

    return ProfileOut(id=profile.id, name=profile.name, journal_ids=[j.id for j in journals], is_default=profile.is_default)


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

    journals = []
    existing_ids = set()

    # Fetch existing journals by ID
    if data.journal_ids:
        journal_result = await db.execute(
            select(Journal).where(Journal.id.in_(data.journal_ids))
        )
        journals = journal_result.scalars().all()
        existing_ids = {j.id for j in journals}

    # Create new journals from PubMed (if they don't exist)
    for new_j in data.new_journals:
        existing = None
        if new_j.issn:
            result = await db.execute(select(Journal).where(Journal.issn == new_j.issn))
            existing = result.scalar_one_or_none()

        if existing:
            if existing.id not in existing_ids:
                journals.append(existing)
                existing_ids.add(existing.id)
        else:
            journal = Journal(
                name=new_j.name,
                issn=new_j.issn,
                iso_abbreviation=new_j.iso_abbreviation,
                category="Custom",
            )
            db.add(journal)
            await db.flush()
            journals.append(journal)
            existing_ids.add(journal.id)

    profile.name = data.name
    profile.journals = journals
    await db.commit()
    await db.refresh(profile)

    return ProfileOut(id=profile.id, name=profile.name, journal_ids=[j.id for j in profile.journals], is_default=profile.is_default)


@router.post("/{profile_id}/set-default", response_model=ProfileOut)
async def set_default_profile(
    profile_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set a profile as the default profile for the user."""
    # Verify profile belongs to user
    result = await db.execute(
        select(Profile)
        .options(selectinload(Profile.journals))
        .where(Profile.id == profile_id, Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Set all user's profiles to not default
    await db.execute(
        Profile.__table__.update()
        .where(Profile.user_id == current_user.id)
        .values(is_default=False)
    )

    # Set the target profile as default
    profile.is_default = True
    await db.commit()
    await db.refresh(profile)

    return ProfileOut(id=profile.id, name=profile.name, journal_ids=[j.id for j in profile.journals], is_default=profile.is_default)


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
