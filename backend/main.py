# MedBrief Backend

import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import auth, journals, profiles, briefs
from app.config import settings
from app.database import engine, Base
from app import models  # noqa: F401 - imports models to register them


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="MedBrief API",
    description="Weekly signals from medical research",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS - allow all origins in production for Railway's random subdomains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for Railway deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(journals.router, prefix="/api/journals", tags=["Journals"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["Profiles"])
app.include_router(briefs.router, prefix="/api/briefs", tags=["Briefs"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Serve frontend static files (if built)
FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve Vue frontend for all non-API routes."""
        # Don't serve frontend for API or auth routes
        if full_path.startswith(("api/", "auth/", "health", "seed")):
            return {"detail": "Not Found"}
        
        # Serve the requested file if it exists
        file_path = FRONTEND_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # Fall back to index.html for SPA routing
        return FileResponse(FRONTEND_DIST / "index.html")


@app.post("/seed")
async def seed_database(reset: bool = False):
    """Seed the database with preset journals. Use reset=true to clear and reseed."""
    from sqlalchemy import select, delete
    from app.database import async_session
    from app.models import Journal
    
    JOURNALS = [
        # Cardiology (10)
        {"name": "Circulation", "issn": "0009-7322", "iso_abbreviation": "Circulation", "category": "Cardiology"},
        {"name": "European Heart Journal", "issn": "0195-668X", "iso_abbreviation": "Eur Heart J", "category": "Cardiology"},
        {"name": "Journal of the American College of Cardiology", "issn": "0735-1097", "iso_abbreviation": "J Am Coll Cardiol", "category": "Cardiology"},
        {"name": "JAMA Cardiology", "issn": "2380-6583", "iso_abbreviation": "JAMA Cardiol", "category": "Cardiology"},
        {"name": "Nature Reviews Cardiology", "issn": "1759-5002", "iso_abbreviation": "Nat Rev Cardiol", "category": "Cardiology"},
        {"name": "Circulation Research", "issn": "0009-7330", "iso_abbreviation": "Circ Res", "category": "Cardiology"},
        {"name": "Heart", "issn": "1355-6037", "iso_abbreviation": "Heart", "category": "Cardiology"},
        {"name": "Cardiovascular Research", "issn": "0008-6363", "iso_abbreviation": "Cardiovasc Res", "category": "Cardiology"},
        {"name": "European Journal of Heart Failure", "issn": "1388-9842", "iso_abbreviation": "Eur J Heart Fail", "category": "Cardiology"},
        {"name": "JACC Heart Failure", "issn": "2213-1779", "iso_abbreviation": "JACC Heart Fail", "category": "Cardiology"},
        
        # Medicine (10)
        {"name": "New England Journal of Medicine", "issn": "0028-4793", "iso_abbreviation": "N Engl J Med", "category": "Medicine"},
        {"name": "The Lancet", "issn": "0140-6736", "iso_abbreviation": "Lancet", "category": "Medicine"},
        {"name": "JAMA", "issn": "0098-7484", "iso_abbreviation": "JAMA", "category": "Medicine"},
        {"name": "BMJ", "issn": "0959-8138", "iso_abbreviation": "BMJ", "category": "Medicine"},
        {"name": "Nature Medicine", "issn": "1078-8956", "iso_abbreviation": "Nat Med", "category": "Medicine"},
        {"name": "Annals of Internal Medicine", "issn": "0003-4819", "iso_abbreviation": "Ann Intern Med", "category": "Medicine"},
        {"name": "PLOS Medicine", "issn": "1549-1676", "iso_abbreviation": "PLoS Med", "category": "Medicine"},
        {"name": "JAMA Internal Medicine", "issn": "2168-6106", "iso_abbreviation": "JAMA Intern Med", "category": "Medicine"},
        {"name": "Journal of Clinical Investigation", "issn": "0021-9738", "iso_abbreviation": "J Clin Invest", "category": "Medicine"},
        {"name": "The Lancet Global Health", "issn": "2214-109X", "iso_abbreviation": "Lancet Glob Health", "category": "Medicine"},
        
        # Oncology (10)
        {"name": "Journal of Clinical Oncology", "issn": "0732-183X", "iso_abbreviation": "J Clin Oncol", "category": "Oncology"},
        {"name": "Lancet Oncology", "issn": "1470-2045", "iso_abbreviation": "Lancet Oncol", "category": "Oncology"},
        {"name": "Nature Reviews Cancer", "issn": "1474-175X", "iso_abbreviation": "Nat Rev Cancer", "category": "Oncology"},
        {"name": "JAMA Oncology", "issn": "2374-2437", "iso_abbreviation": "JAMA Oncol", "category": "Oncology"},
        {"name": "Cancer Cell", "issn": "1535-6108", "iso_abbreviation": "Cancer Cell", "category": "Oncology"},
        {"name": "Annals of Oncology", "issn": "0923-7534", "iso_abbreviation": "Ann Oncol", "category": "Oncology"},
        {"name": "Cancer Research", "issn": "0008-5472", "iso_abbreviation": "Cancer Res", "category": "Oncology"},
        {"name": "Clinical Cancer Research", "issn": "1078-0432", "iso_abbreviation": "Clin Cancer Res", "category": "Oncology"},
        {"name": "Cancer Discovery", "issn": "2159-8274", "iso_abbreviation": "Cancer Discov", "category": "Oncology"},
        {"name": "British Journal of Cancer", "issn": "0007-0920", "iso_abbreviation": "Br J Cancer", "category": "Oncology"},
        
        # Neurology (10)
        {"name": "Lancet Neurology", "issn": "1474-4422", "iso_abbreviation": "Lancet Neurol", "category": "Neurology"},
        {"name": "JAMA Neurology", "issn": "2168-6149", "iso_abbreviation": "JAMA Neurol", "category": "Neurology"},
        {"name": "Nature Neuroscience", "issn": "1097-6256", "iso_abbreviation": "Nat Neurosci", "category": "Neurology"},
        {"name": "Annals of Neurology", "issn": "0364-5134", "iso_abbreviation": "Ann Neurol", "category": "Neurology"},
        {"name": "Brain", "issn": "0006-8950", "iso_abbreviation": "Brain", "category": "Neurology"},
        {"name": "Neurology", "issn": "0028-3878", "iso_abbreviation": "Neurology", "category": "Neurology"},
        {"name": "Nature Reviews Neurology", "issn": "1759-4758", "iso_abbreviation": "Nat Rev Neurol", "category": "Neurology"},
        {"name": "Stroke", "issn": "0039-2499", "iso_abbreviation": "Stroke", "category": "Neurology"},
        {"name": "Journal of Neurology", "issn": "0340-5354", "iso_abbreviation": "J Neurol", "category": "Neurology"},
        {"name": "Movement Disorders", "issn": "0885-3185", "iso_abbreviation": "Mov Disord", "category": "Neurology"},
        
        # Pediatrics (10)
        {"name": "Pediatrics", "issn": "0031-4005", "iso_abbreviation": "Pediatrics", "category": "Pediatrics"},
        {"name": "JAMA Pediatrics", "issn": "2168-6203", "iso_abbreviation": "JAMA Pediatr", "category": "Pediatrics"},
        {"name": "Lancet Child & Adolescent Health", "issn": "2352-4642", "iso_abbreviation": "Lancet Child Adolesc", "category": "Pediatrics"},
        {"name": "Journal of Pediatrics", "issn": "0022-3476", "iso_abbreviation": "J Pediatr", "category": "Pediatrics"},
        {"name": "Archives of Disease in Childhood", "issn": "0003-9888", "iso_abbreviation": "Arch Dis Child", "category": "Pediatrics"},
        {"name": "Pediatric Research", "issn": "0031-3998", "iso_abbreviation": "Pediatr Res", "category": "Pediatrics"},
        {"name": "Journal of Pediatric Surgery", "issn": "0022-3468", "iso_abbreviation": "J Pediatr Surg", "category": "Pediatrics"},
        {"name": "Acta Paediatrica", "issn": "0803-5253", "iso_abbreviation": "Acta Paediatr", "category": "Pediatrics"},
        {"name": "Pediatric Infectious Disease Journal", "issn": "0891-3668", "iso_abbreviation": "Pediatr Infect Dis J", "category": "Pediatrics"},
        {"name": "Journal of Pediatric Gastroenterology and Nutrition", "issn": "0277-2116", "iso_abbreviation": "J Pediatr Gastroenterol Nutr", "category": "Pediatrics"},
        
        # Surgery (10)
        {"name": "Annals of Surgery", "issn": "0003-4932", "iso_abbreviation": "Ann Surg", "category": "Surgery"},
        {"name": "JAMA Surgery", "issn": "2168-6254", "iso_abbreviation": "JAMA Surg", "category": "Surgery"},
        {"name": "British Journal of Surgery", "issn": "0007-1323", "iso_abbreviation": "Br J Surg", "category": "Surgery"},
        {"name": "Lancet Surgery", "issn": "2666-5204", "iso_abbreviation": "Lancet Surg", "category": "Surgery"},
        {"name": "Journal of the American College of Surgeons", "issn": "1072-7515", "iso_abbreviation": "J Am Coll Surg", "category": "Surgery"},
        {"name": "Surgery", "issn": "0039-6060", "iso_abbreviation": "Surgery", "category": "Surgery"},
        {"name": "Annals of Surgical Oncology", "issn": "1068-9265", "iso_abbreviation": "Ann Surg Oncol", "category": "Surgery"},
        {"name": "Surgical Endoscopy", "issn": "0930-2794", "iso_abbreviation": "Surg Endosc", "category": "Surgery"},
        {"name": "Journal of Trauma and Acute Care Surgery", "issn": "2163-0755", "iso_abbreviation": "J Trauma Acute Care Surg", "category": "Surgery"},
        {"name": "World Journal of Surgery", "issn": "0364-2313", "iso_abbreviation": "World J Surg", "category": "Surgery"},
        
        # Psychiatry (10)
        {"name": "JAMA Psychiatry", "issn": "2168-622X", "iso_abbreviation": "JAMA Psychiatry", "category": "Psychiatry"},
        {"name": "Lancet Psychiatry", "issn": "2215-0366", "iso_abbreviation": "Lancet Psychiatry", "category": "Psychiatry"},
        {"name": "American Journal of Psychiatry", "issn": "0002-953X", "iso_abbreviation": "Am J Psychiatry", "category": "Psychiatry"},
        {"name": "Molecular Psychiatry", "issn": "1359-4184", "iso_abbreviation": "Mol Psychiatry", "category": "Psychiatry"},
        {"name": "Biological Psychiatry", "issn": "0006-3223", "iso_abbreviation": "Biol Psychiatry", "category": "Psychiatry"},
        {"name": "British Journal of Psychiatry", "issn": "0007-1250", "iso_abbreviation": "Br J Psychiatry", "category": "Psychiatry"},
        {"name": "Psychological Medicine", "issn": "0033-2917", "iso_abbreviation": "Psychol Med", "category": "Psychiatry"},
        {"name": "World Psychiatry", "issn": "1723-8617", "iso_abbreviation": "World Psychiatry", "category": "Psychiatry"},
        {"name": "Schizophrenia Bulletin", "issn": "0586-7614", "iso_abbreviation": "Schizophr Bull", "category": "Psychiatry"},
        {"name": "Depression and Anxiety", "issn": "1091-4269", "iso_abbreviation": "Depress Anxiety", "category": "Psychiatry"},
        
        # Emergency (10)
        {"name": "Annals of Emergency Medicine", "issn": "0196-0644", "iso_abbreviation": "Ann Emerg Med", "category": "Emergency"},
        {"name": "Emergency Medicine Journal", "issn": "1472-0205", "iso_abbreviation": "Emerg Med J", "category": "Emergency"},
        {"name": "Academic Emergency Medicine", "issn": "1069-6563", "iso_abbreviation": "Acad Emerg Med", "category": "Emergency"},
        {"name": "Resuscitation", "issn": "0300-9572", "iso_abbreviation": "Resuscitation", "category": "Emergency"},
        {"name": "Journal of Emergency Medicine", "issn": "0736-4679", "iso_abbreviation": "J Emerg Med", "category": "Emergency"},
        {"name": "Critical Care Medicine", "issn": "0090-3493", "iso_abbreviation": "Crit Care Med", "category": "Emergency"},
        {"name": "Intensive Care Medicine", "issn": "0342-4642", "iso_abbreviation": "Intensive Care Med", "category": "Emergency"},
        {"name": "American Journal of Emergency Medicine", "issn": "0735-6757", "iso_abbreviation": "Am J Emerg Med", "category": "Emergency"},
        {"name": "Prehospital Emergency Care", "issn": "1090-3127", "iso_abbreviation": "Prehosp Emerg Care", "category": "Emergency"},
        {"name": "Western Journal of Emergency Medicine", "issn": "1936-900X", "iso_abbreviation": "West J Emerg Med", "category": "Emergency"},
    ]
    
    async with async_session() as session:
        if reset:
            # Clear existing journals
            await session.execute(delete(Journal))
            await session.commit()
        else:
            # Check if already seeded
            result = await session.execute(select(Journal).limit(1))
            if result.scalar_one_or_none():
                return {"message": "Database already seeded. Use reset=true to reseed.", "count": 0}
        
        for j_data in JOURNALS:
            journal = Journal(**j_data)
            session.add(journal)
        await session.commit()
    
    return {"message": "Seeded successfully", "count": len(JOURNALS)}

