"""
Seed data for preset journals (Top 10 Cardiology and Top 10 Medicine).
Run this script to populate the database with initial journal data.
"""
import asyncio
from app.database import engine, async_session, Base
from app.models import Journal

# Top 10 Cardiology Journals (by Impact Factor / Prestige)
CARDIOLOGY_JOURNALS = [
    {"name": "Circulation", "issn": "0009-7322", "iso_abbreviation": "Circulation", "category": "Cardiology"},
    {"name": "European Heart Journal", "issn": "0195-668X", "iso_abbreviation": "Eur Heart J", "category": "Cardiology"},
    {"name": "Journal of the American College of Cardiology", "issn": "0735-1097", "iso_abbreviation": "J Am Coll Cardiol", "category": "Cardiology"},
    {"name": "JACC: Cardiovascular Interventions", "issn": "1936-8798", "iso_abbreviation": "JACC Cardiovasc Interv", "category": "Cardiology"},
    {"name": "Circulation Research", "issn": "0009-7330", "iso_abbreviation": "Circ Res", "category": "Cardiology"},
    {"name": "JAMA Cardiology", "issn": "2380-6583", "iso_abbreviation": "JAMA Cardiol", "category": "Cardiology"},
    {"name": "Nature Reviews Cardiology", "issn": "1759-5002", "iso_abbreviation": "Nat Rev Cardiol", "category": "Cardiology"},
    {"name": "Heart", "issn": "1355-6037", "iso_abbreviation": "Heart", "category": "Cardiology"},
    {"name": "Cardiovascular Research", "issn": "0008-6363", "iso_abbreviation": "Cardiovasc Res", "category": "Cardiology"},
    {"name": "European Journal of Heart Failure", "issn": "1388-9842", "iso_abbreviation": "Eur J Heart Fail", "category": "Cardiology"},
]

# Top 10 General Medicine Journals
MEDICINE_JOURNALS = [
    {"name": "New England Journal of Medicine", "issn": "0028-4793", "iso_abbreviation": "N Engl J Med", "category": "Medicine"},
    {"name": "The Lancet", "issn": "0140-6736", "iso_abbreviation": "Lancet", "category": "Medicine"},
    {"name": "JAMA", "issn": "0098-7484", "iso_abbreviation": "JAMA", "category": "Medicine"},
    {"name": "BMJ", "issn": "0959-8138", "iso_abbreviation": "BMJ", "category": "Medicine"},
    {"name": "Annals of Internal Medicine", "issn": "0003-4819", "iso_abbreviation": "Ann Intern Med", "category": "Medicine"},
    {"name": "Nature Medicine", "issn": "1078-8956", "iso_abbreviation": "Nat Med", "category": "Medicine"},
    {"name": "PLOS Medicine", "issn": "1549-1676", "iso_abbreviation": "PLoS Med", "category": "Medicine"},
    {"name": "The Lancet Infectious Diseases", "issn": "1473-3099", "iso_abbreviation": "Lancet Infect Dis", "category": "Medicine"},
    {"name": "Journal of Clinical Investigation", "issn": "0021-9738", "iso_abbreviation": "J Clin Invest", "category": "Medicine"},
    {"name": "JAMA Internal Medicine", "issn": "2168-6106", "iso_abbreviation": "JAMA Intern Med", "category": "Medicine"},
]


async def seed_journals():
    """Create tables and seed journals."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        for j_data in CARDIOLOGY_JOURNALS + MEDICINE_JOURNALS:
            journal = Journal(**j_data)
            session.add(journal)
        await session.commit()
        print(f"Seeded {len(CARDIOLOGY_JOURNALS) + len(MEDICINE_JOURNALS)} journals.")


if __name__ == "__main__":
    asyncio.run(seed_journals())
