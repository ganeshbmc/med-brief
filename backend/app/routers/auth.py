from typing import Dict, Optional
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User
from app.config import settings
from app.services.email import send_password_reset_email

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class MessageResponse(BaseModel):
    message: str


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    token = create_access_token({"sub": str(db_user.id)})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form.username))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user.previous_login_at = user.last_login_at
    user.last_login_at = datetime.utcnow()
    await db.commit()
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# User Profile Endpoints

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    preferences: Optional[Dict] = None
    last_login_at: datetime | None = None
    previous_login_at: datetime | None = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: str


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.full_name = user_update.full_name
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Request password reset email."""
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    # Always return success to prevent email enumeration
    message = "If an account exists, a password reset link has been sent."

    if user:
        # Generate secure reset token
        token = secrets.token_urlsafe(48)
        expires_at = datetime.utcnow() + timedelta(hours=settings.RESET_TOKEN_EXPIRE_HOURS)

        user.reset_token = token
        user.reset_token_expires_at = expires_at
        await db.commit()

        # Build reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        # Send email
        await send_password_reset_email(user.email, reset_link)

    return MessageResponse(message=message)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Reset password with valid token."""
    result = await db.execute(
        select(User).where(
            User.reset_token == request.token,
            User.reset_token_expires_at > datetime.utcnow()
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    # Update password
    user.password_hash = pwd_context.hash(request.new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    await db.commit()

    return MessageResponse(message="Password reset successfully. You can now log in.")
