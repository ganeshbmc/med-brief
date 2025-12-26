from sqlalchemy import Column, Integer, String, ForeignKey, Table
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
    password_hash = Column(String, nullable=False)

    profiles = relationship("Profile", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="My Brief")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

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
