from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship

from app.database import Base

# Association table for Profile <-> Journal (many-to-many)
profile_journals = Table(
    "profile_journals",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id"), primary_key=True),
    Column("journal_id", Integer, ForeignKey("journals.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    preferences = Column(JSON, nullable=True)
    reset_token = Column(String(64), nullable=True)
    reset_token_expires_at = Column(DateTime, nullable=True)

    profiles = relationship("Profile", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="My Brief")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="profiles")
    journals = relationship("Journal", secondary=profile_journals, back_populates="profiles")


class Journal(Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    issn = Column(String, unique=True, index=True)
    iso_abbreviation = Column(String)
    category = Column(String)  # e.g., "Cardiology", "Medicine"

    profiles = relationship("Profile", secondary=profile_journals, back_populates="journals")
