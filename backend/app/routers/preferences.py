from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Literal

from app.database import get_db
from app.models import User
from app.routers.auth import get_current_user

router = APIRouter()


class UserPreferences(BaseModel):
    fontSize: Literal["small", "medium", "large"] = "medium"
    lineSpacing: Literal["normal", "relaxed"] = "normal"
    defaultDays: Literal[3, 7, 14, 30] = 7


class UserPreferencesOut(BaseModel):
    fontSize: str
    lineSpacing: str
    defaultDays: int

    class Config:
        from_attributes = True


@router.get("/", response_model=UserPreferences)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's preferences with defaults."""
    if current_user.preferences:
        return UserPreferences(**current_user.preferences)
    return UserPreferences()


@router.put("/", response_model=UserPreferences)
async def update_preferences(
    prefs: UserPreferences,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user's preferences."""
    current_user.preferences = prefs.model_dump()
    await db.commit()
    await db.refresh(current_user)
    return prefs
