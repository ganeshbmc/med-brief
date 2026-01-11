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
    # Database tables are managed by Alembic migrations
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="MedBrief API",
    description="Weekly signals from medical research",
    version="0.1.0",
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
# Check Docker path first (/app/static), then local dev path
STATIC_DIR = Path(__file__).parent / "static"  # Docker: /app/static
if not STATIC_DIR.exists():
    STATIC_DIR = Path(__file__).parent.parent / "frontend" / "dist"  # Dev: ../frontend/dist

if STATIC_DIR.exists():
    # Mount assets directory
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve Vue frontend for all non-API routes."""
        # Don't serve frontend for API or auth routes
        if full_path.startswith(("api/", "auth/", "health", "seed")):
            return {"detail": "Not Found"}
        
        # Serve the requested file if it exists
        file_path = STATIC_DIR / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # Fall back to index.html for SPA routing
        return FileResponse(STATIC_DIR / "index.html")


@app.post("/seed")
async def seed_database(reset: bool = False):
    """Seed the database with preset journals.
    
    The 'reset' parameter is deprecated and ignored.
    This function now performs a safe upsert (Update/Insert) based on ISSN,
    preserving existing journal IDs and user profile associations.
    """
    from sqlalchemy import select
    from app.database import async_session
    from app.models import Journal
    
    JOURNALS = [
        # --- Medicine (General Internal Medicine) ---
        {"name": "New England Journal of Medicine", "issn": "0028-4793", "iso_abbreviation": "N Engl J Med", "category": "Medicine"},
        {"name": "The Lancet", "issn": "0140-6736", "iso_abbreviation": "Lancet", "category": "Medicine"},
        {"name": "JAMA", "issn": "0098-7484", "iso_abbreviation": "JAMA", "category": "Medicine"},
        {"name": "BMJ", "issn": "0959-8138", "iso_abbreviation": "BMJ", "category": "Medicine"},
        {"name": "Annals of Internal Medicine", "issn": "0003-4819", "iso_abbreviation": "Ann Intern Med", "category": "Medicine"},
        {"name": "JAMA Internal Medicine", "issn": "2168-6106", "iso_abbreviation": "JAMA Intern Med", "category": "Medicine"},
        {"name": "Nature Medicine", "issn": "1078-8956", "iso_abbreviation": "Nat Med", "category": "Medicine"},
        {"name": "PLOS Medicine", "issn": "1549-1676", "iso_abbreviation": "PLoS Med", "category": "Medicine"},
        {"name": "Journal of Internal Medicine", "issn": "0954-6820", "iso_abbreviation": "J Intern Med", "category": "Medicine"},
        {"name": "Mayo Clinic Proceedings", "issn": "0025-6196", "iso_abbreviation": "Mayo Clin Proc", "category": "Medicine"},
        {"name": "American Journal of Medicine", "issn": "0002-9343", "iso_abbreviation": "Am J Med", "category": "Medicine"},
        {"name": "Cleveland Clinic Journal of Medicine", "issn": "0891-1150", "iso_abbreviation": "Cleve Clin J Med", "category": "Medicine"},
        {"name": "CMAJ (Canadian Medical Association Journal)", "issn": "0820-3946", "iso_abbreviation": "CMAJ", "category": "Medicine"},
        {"name": "Medical Journal of Australia", "issn": "0025-729X", "iso_abbreviation": "Med J Aust", "category": "Medicine"},
        {"name": "The Lancet Global Health", "issn": "2214-109X", "iso_abbreviation": "Lancet Glob Health", "category": "Medicine"},
        {"name": "Journal of Clinical Investigation", "issn": "0021-9738", "iso_abbreviation": "J Clin Invest", "category": "Medicine"},
        {"name": "Science Translational Medicine", "issn": "1946-6234", "iso_abbreviation": "Sci Transl Med", "category": "Medicine"},
        {"name": "BMC Medicine", "issn": "1741-7015", "iso_abbreviation": "BMC Med", "category": "Medicine"},
        {"name": "EClinicalMedicine", "issn": "2589-5370", "iso_abbreviation": "EClinicalMedicine", "category": "Medicine"},
        {"name": "Journal of Hospital Medicine", "issn": "1553-5592", "iso_abbreviation": "J Hosp Med", "category": "Medicine"},

        # --- Cardiology ---
        {"name": "Circulation", "issn": "0009-7322", "iso_abbreviation": "Circulation", "category": "Cardiology"},
        {"name": "Journal of the American College of Cardiology", "issn": "0735-1097", "iso_abbreviation": "J Am Coll Cardiol", "category": "Cardiology"},
        {"name": "European Heart Journal", "issn": "0195-668X", "iso_abbreviation": "Eur Heart J", "category": "Cardiology"},
        {"name": "JAMA Cardiology", "issn": "2380-6583", "iso_abbreviation": "JAMA Cardiol", "category": "Cardiology"},
        {"name": "Nature Reviews Cardiology", "issn": "1759-5002", "iso_abbreviation": "Nat Rev Cardiol", "category": "Cardiology"},
        {"name": "Circulation Research", "issn": "0009-7330", "iso_abbreviation": "Circ Res", "category": "Cardiology"},
        {"name": "JACC: Heart Failure", "issn": "2213-1779", "iso_abbreviation": "JACC Heart Fail", "category": "Cardiology"},
        {"name": "JACC: Cardiovascular Interventions", "issn": "1936-8798", "iso_abbreviation": "JACC Cardiovasc Interv", "category": "Cardiology"},
        {"name": "JACC: Cardiovascular Imaging", "issn": "1936-878X", "iso_abbreviation": "JACC Cardiovasc Imaging", "category": "Cardiology"},
        {"name": "European Journal of Heart Failure", "issn": "1388-9842", "iso_abbreviation": "Eur J Heart Fail", "category": "Cardiology"},
        {"name": "Heart", "issn": "1355-6037", "iso_abbreviation": "Heart", "category": "Cardiology"},
        {"name": "Cardiovascular Research", "issn": "0008-6363", "iso_abbreviation": "Cardiovasc Res", "category": "Cardiology"},
        {"name": "Europace", "issn": "1099-5129", "iso_abbreviation": "Europace", "category": "Cardiology"},
        {"name": "Heart Rhythm", "issn": "1547-5271", "iso_abbreviation": "Heart Rhythm", "category": "Cardiology"},
        {"name": "Circulation: Heart Failure", "issn": "1941-3289", "iso_abbreviation": "Circ Heart Fail", "category": "Cardiology"},
        {"name": "American Journal of Cardiology", "issn": "0002-9149", "iso_abbreviation": "Am J Cardiol", "category": "Cardiology"},
        {"name": "Chest", "issn": "0012-3692", "iso_abbreviation": "Chest", "category": "Cardiology"}, # Also Pulm/Crit Care
        {"name": "JACC: Clinical Electrophysiology", "issn": "2405-500X", "iso_abbreviation": "JACC Clin Electrophysiol", "category": "Cardiology"},
        {"name": "European Heart Journal - Cardiovascular Pharmacotherapy", "issn": "2055-6837", "iso_abbreviation": "Eur Heart J Cardiovasc Pharmacother", "category": "Cardiology"},
        {"name": "Clinical Research in Cardiology", "issn": "1861-0684", "iso_abbreviation": "Clin Res Cardiol", "category": "Cardiology"},

        # --- Oncology ---
        {"name": "Journal of Clinical Oncology", "issn": "0732-183X", "iso_abbreviation": "J Clin Oncol", "category": "Oncology"},
        {"name": "The Lancet Oncology", "issn": "1470-2045", "iso_abbreviation": "Lancet Oncol", "category": "Oncology"},
        {"name": "Cancer Cell", "issn": "1535-6108", "iso_abbreviation": "Cancer Cell", "category": "Oncology"},
        {"name": "Cancer Discovery", "issn": "2159-8274", "iso_abbreviation": "Cancer Discov", "category": "Oncology"},
        {"name": "Nature Reviews Cancer", "issn": "1474-175X", "iso_abbreviation": "Nat Rev Cancer", "category": "Oncology"},
        {"name": "JAMA Oncology", "issn": "2374-2437", "iso_abbreviation": "JAMA Oncol", "category": "Oncology"},
        {"name": "Annals of Oncology", "issn": "0923-7534", "iso_abbreviation": "Ann Oncol", "category": "Oncology"},
        {"name": "Clinical Cancer Research", "issn": "1078-0432", "iso_abbreviation": "Clin Cancer Res", "category": "Oncology"},
        {"name": "Cancer Research", "issn": "0008-5472", "iso_abbreviation": "Cancer Res", "category": "Oncology"},
        {"name": "Journal of the National Cancer Institute", "issn": "0027-8874", "iso_abbreviation": "J Natl Cancer Inst", "category": "Oncology"},
        {"name": "Leukemia", "issn": "0887-6924", "iso_abbreviation": "Leukemia", "category": "Oncology"},
        {"name": "Blood", "issn": "0006-4971", "iso_abbreviation": "Blood", "category": "Oncology"},
        {"name": "Journal of Thoracic Oncology", "issn": "1556-0864", "iso_abbreviation": "J Thorac Oncol", "category": "Oncology"},
        {"name": "European Journal of Cancer", "issn": "0959-8049", "iso_abbreviation": "Eur J Cancer", "category": "Oncology"},
        {"name": "British Journal of Cancer", "issn": "0007-0920", "iso_abbreviation": "Br J Cancer", "category": "Oncology"},
        {"name": "Seminars in Oncology", "issn": "0093-7754", "iso_abbreviation": "Semin Oncol", "category": "Oncology"},
        {"name": "The Oncologist", "issn": "1083-7159", "iso_abbreviation": "Oncologist", "category": "Oncology"},
        {"name": "Cancer", "issn": "0008-543X", "iso_abbreviation": "Cancer", "category": "Oncology"},
        {"name": "Molecular Cancer Therapeutics", "issn": "1535-7163", "iso_abbreviation": "Mol Cancer Ther", "category": "Oncology"},
        {"name": "Breast Cancer Research", "issn": "1465-5411", "iso_abbreviation": "Breast Cancer Res", "category": "Oncology"},

        # --- Neurology ---
        {"name": "Lancet Neurology", "issn": "1474-4422", "iso_abbreviation": "Lancet Neurol", "category": "Neurology"},
        {"name": "Nature Reviews Neurology", "issn": "1759-4758", "iso_abbreviation": "Nat Rev Neurol", "category": "Neurology"},
        {"name": "JAMA Neurology", "issn": "2168-6149", "iso_abbreviation": "JAMA Neurol", "category": "Neurology"},
        {"name": "Brain", "issn": "0006-8950", "iso_abbreviation": "Brain", "category": "Neurology"},
        {"name": "Annals of Neurology", "issn": "0364-5134", "iso_abbreviation": "Ann Neurol", "category": "Neurology"},
        {"name": "Neurology", "issn": "0028-3878", "iso_abbreviation": "Neurology", "category": "Neurology"},
        {"name": "Stroke", "issn": "0039-2499", "iso_abbreviation": "Stroke", "category": "Neurology"},
        {"name": "Nature Neuroscience", "issn": "1097-6256", "iso_abbreviation": "Nat Neurosci", "category": "Neurology"},
        {"name": "Neuron", "issn": "0896-6273", "iso_abbreviation": "Neuron", "category": "Neurology"},
        {"name": "Acta Neuropathologica", "issn": "0001-6322", "iso_abbreviation": "Acta Neuropathol", "category": "Neurology"},
        {"name": "Journal of Neurology, Neurosurgery & Psychiatry", "issn": "0022-3050", "iso_abbreviation": "J Neurol Neurosurg Psychiatry", "category": "Neurology"},
        {"name": "Movement Disorders", "issn": "0885-3185", "iso_abbreviation": "Mov Disord", "category": "Neurology"},
        {"name": "Epilepsia", "issn": "0013-9580", "iso_abbreviation": "Epilepsia", "category": "Neurology"},
        {"name": "Neurobiology of Disease", "issn": "0969-9961", "iso_abbreviation": "Neurobiol Dis", "category": "Neurology"},
        {"name": "Journal of Neurology", "issn": "0340-5354", "iso_abbreviation": "J Neurol", "category": "Neurology"},
        {"name": "European Journal of Neurology", "issn": "1351-5101", "iso_abbreviation": "Eur J Neurol", "category": "Neurology"},
        {"name": "Alzheimer's & Dementia", "issn": "1552-5260", "iso_abbreviation": "Alzheimers Dement", "category": "Neurology"},
        {"name": "Current Opinion in Neurology", "issn": "1350-7540", "iso_abbreviation": "Curr Opin Neurol", "category": "Neurology"},
        {"name": "Pain", "issn": "0304-3959", "iso_abbreviation": "Pain", "category": "Neurology"},
        {"name": "Cephalalgia", "issn": "0333-1024", "iso_abbreviation": "Cephalalgia", "category": "Neurology"},

        # --- Pediatrics ---
        {"name": "Pediatrics", "issn": "0031-4005", "iso_abbreviation": "Pediatrics", "category": "Pediatrics"},
        {"name": "JAMA Pediatrics", "issn": "2168-6203", "iso_abbreviation": "JAMA Pediatr", "category": "Pediatrics"},
        {"name": "The Lancet Child & Adolescent Health", "issn": "2352-4642", "iso_abbreviation": "Lancet Child Adolesc", "category": "Pediatrics"},
        {"name": "Journal of Pediatrics", "issn": "0022-3476", "iso_abbreviation": "J Pediatr", "category": "Pediatrics"},
        {"name": "Archives of Disease in Childhood", "issn": "0003-9888", "iso_abbreviation": "Arch Dis Child", "category": "Pediatrics"},
        {"name": "Pediatric Research", "issn": "0031-3998", "iso_abbreviation": "Pediatr Res", "category": "Pediatrics"},
        {"name": "Journal of Adolescent Health", "issn": "1054-139X", "iso_abbreviation": "J Adolesc Health", "category": "Pediatrics"},
        {"name": "Pediatric Infectious Disease Journal", "issn": "0891-3668", "iso_abbreviation": "Pediatr Infect Dis J", "category": "Pediatrics"},
        {"name": "Journal of Pediatric Gastroenterology and Nutrition", "issn": "0277-2116", "iso_abbreviation": "J Pediatr Gastroenterol Nutr", "category": "Pediatrics"},
        {"name": "Pediatric Critical Care Medicine", "issn": "1529-7535", "iso_abbreviation": "Pediatr Crit Care Med", "category": "Pediatrics"},
        {"name": "Pediatric Allergy and Immunology", "issn": "0905-6157", "iso_abbreviation": "Pediatr Allergy Immunol", "category": "Pediatrics"},
        {"name": "Acta Paediatrica", "issn": "0803-5253", "iso_abbreviation": "Acta Paediatr", "category": "Pediatrics"},
        {"name": "European Journal of Pediatrics", "issn": "0340-6199", "iso_abbreviation": "Eur J Pediatr", "category": "Pediatrics"},
        {"name": "Pediatric Pulmonology", "issn": "8755-6863", "iso_abbreviation": "Pediatr Pulmonol", "category": "Pediatrics"},
        {"name": "Journal of Pediatric Hematology/Oncology", "issn": "1077-4114", "iso_abbreviation": "J Pediatr Hematol Oncol", "category": "Pediatrics"},
        {"name": "Academic Pediatrics", "issn": "1876-2859", "iso_abbreviation": "Acad Pediatr", "category": "Pediatrics"},
        {"name": "Pediatric Nephrology", "issn": "0931-041X", "iso_abbreviation": "Pediatr Nephrol", "category": "Pediatrics"},
        {"name": "Pediatric Diabetes", "issn": "1399-543X", "iso_abbreviation": "Pediatr Diabetes", "category": "Pediatrics"},
        {"name": "Journal of Child Psychology and Psychiatry", "issn": "0021-9630", "iso_abbreviation": "J Child Psychol Psychiatry", "category": "Pediatrics"},
        {"name": "Neonatology", "issn": "1661-7800", "iso_abbreviation": "Neonatology", "category": "Pediatrics"},

        # --- Surgery (General & Subspecialties not covered elsewhere) ---
        {"name": "Annals of Surgery", "issn": "0003-4932", "iso_abbreviation": "Ann Surg", "category": "Surgery"},
        {"name": "JAMA Surgery", "issn": "2168-6254", "iso_abbreviation": "JAMA Surg", "category": "Surgery"},
        {"name": "British Journal of Surgery", "issn": "0007-1323", "iso_abbreviation": "Br J Surg", "category": "Surgery"},
        {"name": "Journal of the American College of Surgeons", "issn": "1072-7515", "iso_abbreviation": "J Am Coll Surg", "category": "Surgery"},
        {"name": "Surgery", "issn": "0039-6060", "iso_abbreviation": "Surgery", "category": "Surgery"},
        {"name": "World Journal of Surgery", "issn": "0364-2313", "iso_abbreviation": "World J Surg", "category": "Surgery"},
        {"name": "Journal of Trauma and Acute Care Surgery", "issn": "2163-0755", "iso_abbreviation": "J Trauma Acute Care Surg", "category": "Surgery"},
        {"name": "Surgical Endoscopy", "issn": "0930-2794", "iso_abbreviation": "Surg Endosc", "category": "Surgery"},
        {"name": "Journal of Gastrointestinal Surgery", "issn": "1091-255X", "iso_abbreviation": "J Gastrointest Surg", "category": "Surgery"},
        {"name": "Journal of Vascular Surgery", "issn": "0741-5214", "iso_abbreviation": "J Vasc Surg", "category": "Surgery"},
        {"name": "Annals of Thoracic Surgery", "issn": "0003-4975", "iso_abbreviation": "Ann Thorac Surg", "category": "Surgery"},
        {"name": "Journal of Thoracic and Cardiovascular Surgery", "issn": "0022-5223", "iso_abbreviation": "J Thorac Cardiovasc Surg", "category": "Surgery"},
        {"name": "European Journal of Vascular and Endovascular Surgery", "issn": "1078-5884", "iso_abbreviation": "Eur J Vasc Endovasc Surg", "category": "Surgery"},
        {"name": "Spine", "issn": "0362-2436", "iso_abbreviation": "Spine", "category": "Surgery"},
        {"name": "Journal of Bone and Joint Surgery (American)", "issn": "0021-9355", "iso_abbreviation": "J Bone Joint Surg Am", "category": "Surgery"},
        {"name": "Journal of Pediatric Surgery", "issn": "0022-3468", "iso_abbreviation": "J Pediatr Surg", "category": "Surgery"},
        {"name": "Diseases of the Colon & Rectum", "issn": "0012-3706", "iso_abbreviation": "Dis Colon Rectum", "category": "Surgery"},
        {"name": "Journal of Neurosurgery", "issn": "0022-3085", "iso_abbreviation": "J Neurosurg", "category": "Surgery"},
        {"name": "Neurosurgery", "issn": "0148-396X", "iso_abbreviation": "Neurosurgery", "category": "Surgery"},
        {"name": "Journal of Heart and Lung Transplantation", "issn": "1053-2498", "iso_abbreviation": "J Heart Lung Transplant", "category": "Surgery"},

        # --- Psychiatry ---
        {"name": "World Psychiatry", "issn": "1723-8617", "iso_abbreviation": "World Psychiatry", "category": "Psychiatry"},
        {"name": "JAMA Psychiatry", "issn": "2168-622X", "iso_abbreviation": "JAMA Psychiatry", "category": "Psychiatry"},
        {"name": "The Lancet Psychiatry", "issn": "2215-0366", "iso_abbreviation": "Lancet Psychiatry", "category": "Psychiatry"},
        {"name": "American Journal of Psychiatry", "issn": "0002-953X", "iso_abbreviation": "Am J Psychiatry", "category": "Psychiatry"},
        {"name": "Molecular Psychiatry", "issn": "1359-4184", "iso_abbreviation": "Mol Psychiatry", "category": "Psychiatry"},
        {"name": "Biological Psychiatry", "issn": "0006-3223", "iso_abbreviation": "Biol Psychiatry", "category": "Psychiatry"},
        {"name": "British Journal of Psychiatry", "issn": "0007-1250", "iso_abbreviation": "Br J Psychiatry", "category": "Psychiatry"},
        {"name": "Schizophrenia Bulletin", "issn": "0586-7614", "iso_abbreviation": "Schizophr Bull", "category": "Psychiatry"},
        {"name": "Psychological Medicine", "issn": "0033-2917", "iso_abbreviation": "Psychol Med", "category": "Psychiatry"},
        {"name": "Journal of Clinical Psychiatry", "issn": "0160-6689", "iso_abbreviation": "J Clin Psychiatry", "category": "Psychiatry"},
        {"name": "Neuropsychopharmacology", "issn": "0893-133X", "iso_abbreviation": "Neuropsychopharmacology", "category": "Psychiatry"},
        {"name": "Journal of Child Psychology and Psychiatry", "issn": "0021-9630", "iso_abbreviation": "J Child Psychol Psychiatry", "category": "Psychiatry"},
        {"name": "Bipolar Disorders", "issn": "1398-5647", "iso_abbreviation": "Bipolar Disord", "category": "Psychiatry"},
        {"name": "Acta Psychiatrica Scandinavica", "issn": "0001-690X", "iso_abbreviation": "Acta Psychiatr Scand", "category": "Psychiatry"},
        {"name": "Journal of Neurology, Neurosurgery & Psychiatry", "issn": "0022-3050", "iso_abbreviation": "J Neurol Neurosurg Psychiatry", "category": "Psychiatry"},
        {"name": "Psychotherapy and Psychosomatics", "issn": "0033-3190", "iso_abbreviation": "Psychother Psychosom", "category": "Psychiatry"},
        {"name": "Journal of the American Academy of Child & Adolescent Psychiatry", "issn": "0890-8567", "iso_abbreviation": "J Am Acad Child Adolesc Psychiatry", "category": "Psychiatry"},
        {"name": "Depression and Anxiety", "issn": "1091-4269", "iso_abbreviation": "Depress Anxiety", "category": "Psychiatry"},
        {"name": "International Journal of Epidemiology", "issn": "0300-5771", "iso_abbreviation": "Int J Epidemiol", "category": "Psychiatry"}, # Often relevant
        {"name": "Addiction", "issn": "0965-2140", "iso_abbreviation": "Addiction", "category": "Psychiatry"},

        # --- Emergency Medicine ---
        {"name": "Annals of Emergency Medicine", "issn": "0196-0644", "iso_abbreviation": "Ann Emerg Med", "category": "Emergency"},
        {"name": "Resuscitation", "issn": "0300-9572", "iso_abbreviation": "Resuscitation", "category": "Emergency"},
        {"name": "Academic Emergency Medicine", "issn": "1069-6563", "iso_abbreviation": "Acad Emerg Med", "category": "Emergency"},
        {"name": "Emergency Medicine Journal", "issn": "1472-0205", "iso_abbreviation": "Emerg Med J", "category": "Emergency"},
        {"name": "Journal of Emergency Medicine", "issn": "0736-4679", "iso_abbreviation": "J Emerg Med", "category": "Emergency"},
        {"name": "American Journal of Emergency Medicine", "issn": "0735-6757", "iso_abbreviation": "Am J Emerg Med", "category": "Emergency"},
        {"name": "Prehospital Emergency Care", "issn": "1090-3127", "iso_abbreviation": "Prehosp Emerg Care", "category": "Emergency"},
        {"name": "Western Journal of Emergency Medicine", "issn": "1936-900X", "iso_abbreviation": "West J Emerg Med", "category": "Emergency"},
        {"name": "Emergency Medicine Australasia", "issn": "1742-6723", "iso_abbreviation": "Emerg Med Australas", "category": "Emergency"},
        {"name": "European Journal of Emergency Medicine", "issn": "0969-9546", "iso_abbreviation": "Eur J Emerg Med", "category": "Emergency"},
        {"name": "Scandinavian Journal of Trauma, Resuscitation and Emergency Medicine", "issn": "1757-7241", "iso_abbreviation": "Scand J Trauma Resusc Emerg Med", "category": "Emergency"},
        {"name": "Injury", "issn": "0020-1383", "iso_abbreviation": "Injury", "category": "Emergency"},
        {"name": "Journal of Trauma and Acute Care Surgery", "issn": "2163-0755", "iso_abbreviation": "J Trauma Acute Care Surg", "category": "Emergency"},
        {"name": "Pediatric Emergency Care", "issn": "0749-5161", "iso_abbreviation": "Pediatr Emerg Care", "category": "Emergency"},
        {"name": "Clinical Toxicology", "issn": "1556-3650", "iso_abbreviation": "Clin Toxicol (Phila)", "category": "Emergency"},
        {"name": "Prehospital and Disaster Medicine", "issn": "1049-023X", "iso_abbreviation": "Prehosp Disaster Med", "category": "Emergency"},
        {"name": "Journal of Emergency Nursing", "issn": "0099-1767", "iso_abbreviation": "J Emerg Nurs", "category": "Emergency"},
        {"name": "Canadian Journal of Emergency Medicine", "issn": "1481-8035", "iso_abbreviation": "CJEM", "category": "Emergency"},
        {"name": "Internal and Emergency Medicine", "issn": "1828-0447", "iso_abbreviation": "Intern Emerg Med", "category": "Emergency"},
        {"name": "World Journal of Emergency Surgery", "issn": "1749-7922", "iso_abbreviation": "World J Emerg Surg", "category": "Emergency"},

        # --- Nephrology ---
        {"name": "Journal of the American Society of Nephrology", "issn": "1046-6673", "iso_abbreviation": "J Am Soc Nephrol", "category": "Nephrology"},
        {"name": "Kidney International", "issn": "0085-2538", "iso_abbreviation": "Kidney Int", "category": "Nephrology"},
        {"name": "Nature Reviews Nephrology", "issn": "1759-5061", "iso_abbreviation": "Nat Rev Nephrol", "category": "Nephrology"},
        {"name": "CJASN (Clinical Journal of the American Society of Nephrology)", "issn": "1555-9041", "iso_abbreviation": "Clin J Am Soc Nephrol", "category": "Nephrology"},
        {"name": "American Journal of Kidney Diseases", "issn": "0272-6386", "iso_abbreviation": "Am J Kidney Dis", "category": "Nephrology"},
        {"name": "Nephrology Dialysis Transplantation", "issn": "0931-0509", "iso_abbreviation": "Nephrol Dial Transplant", "category": "Nephrology"},
        {"name": "Kidney International Supplements", "issn": "2157-1716", "iso_abbreviation": "Kidney Int Suppl", "category": "Nephrology"},
        {"name": "Current Opinion in Nephrology and Hypertension", "issn": "1062-4821", "iso_abbreviation": "Curr Opin Nephrol Hypertens", "category": "Nephrology"},
        {"name": "Seminars in Nephrology", "issn": "0270-9295", "iso_abbreviation": "Semin Nephrol", "category": "Nephrology"},
        {"name": "Clinical Kidney Journal", "issn": "2048-8505", "iso_abbreviation": "Clin Kidney J", "category": "Nephrology"},
        {"name": "BMC Nephrology", "issn": "1471-2369", "iso_abbreviation": "BMC Nephrol", "category": "Nephrology"},
        {"name": "Nephrology", "issn": "1320-5358", "iso_abbreviation": "Nephrology (Carlton)", "category": "Nephrology"},
        {"name": "Journal of Renal Nutrition", "issn": "1051-2276", "iso_abbreviation": "J Ren Nutr", "category": "Nephrology"},
        {"name": "Peritoneal Dialysis International", "issn": "0896-8608", "iso_abbreviation": "Perit Dial Int", "category": "Nephrology"},
        {"name": "American Journal of Physiology-Renal Physiology", "issn": "1931-857X", "iso_abbreviation": "Am J Physiol Renal Physiol", "category": "Nephrology"},
        {"name": "Journal of Nephrology", "issn": "1121-8428", "iso_abbreviation": "J Nephrol", "category": "Nephrology"},
        {"name": "Transplantation", "issn": "0041-1337", "iso_abbreviation": "Transplantation", "category": "Nephrology"}, # Overlap with surgery
        {"name": "American Journal of Transplantation", "issn": "1600-6135", "iso_abbreviation": "Am J Transplant", "category": "Nephrology"},
        {"name": "Pediatric Nephrology", "issn": "0931-041X", "iso_abbreviation": "Pediatr Nephrol", "category": "Nephrology"},
        {"name": "Kidney360", "issn": "2641-7650", "iso_abbreviation": "Kidney360", "category": "Nephrology"},

        # --- Endocrinology ---
        {"name": "Diabetes Care", "issn": "0149-5992", "iso_abbreviation": "Diabetes Care", "category": "Endocrinology"},
        {"name": "The Lancet Diabetes & Endocrinology", "issn": "2213-8587", "iso_abbreviation": "Lancet Diabetes Endocrinol", "category": "Endocrinology"},
        {"name": "Nature Reviews Endocrinology", "issn": "1759-5029", "iso_abbreviation": "Nat Rev Endocrinol", "category": "Endocrinology"},
        {"name": "Journal of Clinical Endocrinology & Metabolism", "issn": "0021-972X", "iso_abbreviation": "J Clin Endocrinol Metab", "category": "Endocrinology"},
        {"name": "Diabetes", "issn": "0012-1797", "iso_abbreviation": "Diabetes", "category": "Endocrinology"},
        {"name": "Diologia", "issn": "0012-186X", "iso_abbreviation": "Diabetologia", "category": "Endocrinology"},
        {"name": "Endocrine Reviews", "issn": "0163-769X", "iso_abbreviation": "Endocr Rev", "category": "Endocrinology"},
        {"name": "Thyroid", "issn": "1050-7256", "iso_abbreviation": "Thyroid", "category": "Endocrinology"},
        {"name": "Journal of Bone and Mineral Research", "issn": "0884-0431", "iso_abbreviation": "J Bone Miner Res", "category": "Endocrinology"},
        {"name": "European Journal of Endocrinology", "issn": "0804-4643", "iso_abbreviation": "Eur J Endocrinol", "category": "Endocrinology"},
        {"name": "Molecular Metabolism", "issn": "2212-8778", "iso_abbreviation": "Mol Metab", "category": "Endocrinology"},
        {"name": "Cell Metabolism", "issn": "1550-4131", "iso_abbreviation": "Cell Metab", "category": "Endocrinology"},
        {"name": "Obesity", "issn": "1930-7381", "iso_abbreviation": "Obesity (Silver Spring)", "category": "Endocrinology"},
        {"name": "Clinical Endocrinology", "issn": "0300-0664", "iso_abbreviation": "Clin Endocrinol (Oxf)", "category": "Endocrinology"},
        {"name": "Diabetes, Obesity and Metabolism", "issn": "1462-8902", "iso_abbreviation": "Diabetes Obes Metab", "category": "Endocrinology"},
        {"name": "Endocrinology", "issn": "0013-7227", "iso_abbreviation": "Endocrinology", "category": "Endocrinology"},
        {"name": "Best Practice & Research Clinical Endocrinology & Metabolism", "issn": "1521-690X", "iso_abbreviation": "Best Pract Res Clin Endocrinol Metab", "category": "Endocrinology"},
        {"name": "Current Opinion in Lipidology", "issn": "0957-9672", "iso_abbreviation": "Curr Opin Lipidol", "category": "Endocrinology"},
        {"name": "Journal of the Endocrine Society", "issn": "2472-1972", "iso_abbreviation": "J Endocr Soc", "category": "Endocrinology"},
        {"name": "Pituitary", "issn": "1386-341X", "iso_abbreviation": "Pituitary", "category": "Endocrinology"},

        # --- Surgical Oncology ---
        {"name": "Annals of Surgical Oncology", "issn": "1068-9265", "iso_abbreviation": "Ann Surg Oncol", "category": "Surgical Oncology"},
        {"name": "Journal of Surgical Oncology", "issn": "0022-4790", "iso_abbreviation": "J Surg Oncol", "category": "Surgical Oncology"},
        {"name": "European Journal of Surgical Oncology", "issn": "0748-7983", "iso_abbreviation": "Eur J Surg Oncol", "category": "Surgical Oncology"},
        {"name": "Surgical Oncology", "issn": "0960-7404", "iso_abbreviation": "Surg Oncol", "category": "Surgical Oncology"},
        {"name": "Surgical Oncology Clinics of North America", "issn": "1055-3207", "iso_abbreviation": "Surg Oncol Clin N Am", "category": "Surgical Oncology"},
        {"name": "World Journal of Surgical Oncology", "issn": "1477-7819", "iso_abbreviation": "World J Surg Oncol", "category": "Surgical Oncology"},
        {"name": "Breast Cancer Research and Treatment", "issn": "0167-6806", "iso_abbreviation": "Breast Cancer Res Treat", "category": "Surgical Oncology"},
        {"name": "HPB", "issn": "1365-182X", "iso_abbreviation": "HPB (Oxford)", "category": "Surgical Oncology"},
        {"name": "Melanoma Research", "issn": "0960-8931", "iso_abbreviation": "Melanoma Res", "category": "Surgical Oncology"},
        {"name": "Sarcoma", "issn": "1357-714X", "iso_abbreviation": "Sarcoma", "category": "Surgical Oncology"},
        {"name": "Endocrine-Related Cancer", "issn": "1351-0088", "iso_abbreviation": "Endocr Relat Cancer", "category": "Surgical Oncology"},
        {"name": "Oral Oncology", "issn": "1368-8375", "iso_abbreviation": "Oral Oncol", "category": "Surgical Oncology"},
        {"name": "Head and Neck", "issn": "1043-3074", "iso_abbreviation": "Head Neck", "category": "Surgical Oncology"},
        {"name": "Gynecologic Oncology", "issn": "0090-8258", "iso_abbreviation": "Gynecol Oncol", "category": "Surgical Oncology"},
        {"name": "Urologic Oncology", "issn": "1078-1439", "iso_abbreviation": "Urol Oncol", "category": "Surgical Oncology"},
        {"name": "Journal of Neuro-Oncology", "issn": "0167-594X", "iso_abbreviation": "J Neurooncol", "category": "Surgical Oncology"},
        {"name": "International Journal of Surgical Oncology", "issn": "2090-1402", "iso_abbreviation": "Int J Surg Oncol", "category": "Surgical Oncology"},
        {"name": "BMC Cancer", "issn": "1471-2407", "iso_abbreviation": "BMC Cancer", "category": "Surgical Oncology"},
        {"name": "American Journal of Clinical Oncology", "issn": "0277-3732", "iso_abbreviation": "Am J Clin Oncol", "category": "Surgical Oncology"},
        {"name": "Clinical & Experimental Metastasis", "issn": "0262-0898", "iso_abbreviation": "Clin Exp Metastasis", "category": "Surgical Oncology"},

        # --- Critical Care Medicine ---
        {"name": "Critical Care Medicine", "issn": "0090-3493", "iso_abbreviation": "Crit Care Med", "category": "Critical Care"},
        {"name": "Intensive Care Medicine", "issn": "0342-4642", "iso_abbreviation": "Intensive Care Med", "category": "Critical Care"},
        {"name": "American Journal of Respiratory and Critical Care Medicine", "issn": "1073-449X", "iso_abbreviation": "Am J Respir Crit Care Med", "category": "Critical Care"},
        {"name": "The Lancet Respiratory Medicine", "issn": "2213-2600", "iso_abbreviation": "Lancet Respir Med", "category": "Critical Care"},
        {"name": "Chest", "issn": "0012-3692", "iso_abbreviation": "Chest", "category": "Critical Care"},
        {"name": "Critical Care", "issn": "1364-8535", "iso_abbreviation": "Crit Care", "category": "Critical Care"},
        {"name": "Annals of Intensive Care", "issn": "2110-5820", "iso_abbreviation": "Ann Intensive Care", "category": "Critical Care"},
        {"name": "Journal of Critical Care", "issn": "0883-9441", "iso_abbreviation": "J Crit Care", "category": "Critical Care"},
        {"name": "Current Opinion in Critical Care", "issn": "1070-5295", "iso_abbreviation": "Curr Opin Crit Care", "category": "Critical Care"},
        {"name": "Shock", "issn": "1073-2322", "iso_abbreviation": "Shock", "category": "Critical Care"},
        {"name": "Journal of Trauma and Acute Care Surgery", "issn": "2163-0755", "iso_abbreviation": "J Trauma Acute Care Surg", "category": "Critical Care"},
        {"name": "Anaesthesia", "issn": "0003-2409", "iso_abbreviation": "Anaesthesia", "category": "Critical Care"},
        {"name": "Anesthesiology", "issn": "0003-3022", "iso_abbreviation": "Anesthesiology", "category": "Critical Care"},
        {"name": "British Journal of Anaesthesia", "issn": "0007-0912", "iso_abbreviation": "Br J Anaesth", "category": "Critical Care"},
        {"name": "Neurocritical Care", "issn": "1541-6933", "iso_abbreviation": "Neurocrit Care", "category": "Critical Care"},
        {"name": "Pediatric Critical Care Medicine", "issn": "1529-7535", "iso_abbreviation": "Pediatr Crit Care Med", "category": "Critical Care"},
        {"name": "Resuscitation", "issn": "0300-9572", "iso_abbreviation": "Resuscitation", "category": "Critical Care"},
        {"name": "Journal of Intensive Care", "issn": "2052-0492", "iso_abbreviation": "J Intensive Care", "category": "Critical Care"},
        {"name": "Minerva Anestesiologica", "issn": "0375-9393", "iso_abbreviation": "Minerva Anestesiol", "category": "Critical Care"},
        {"name": "Australian Critical Care", "issn": "1036-7314", "iso_abbreviation": "Aust Crit Care", "category": "Critical Care"},

        # --- Plastic Surgery ---
        {"name": "Plastic and Reconstructive Surgery", "issn": "0032-1052", "iso_abbreviation": "Plast Reconstr Surg", "category": "Plastic Surgery"},
        {"name": "JAMA Facial Plastic Surgery", "issn": "2168-6076", "iso_abbreviation": "JAMA Facial Plast Surg", "category": "Plastic Surgery"}, # Now Facial Plastic Surgery & Aesthetic Medicine
        {"name": "Aesthetic Surgery Journal", "issn": "1090-820X", "iso_abbreviation": "Aesthet Surg J", "category": "Plastic Surgery"},
        {"name": "Journal of Plastic, Reconstructive & Aesthetic Surgery", "issn": "1748-6815", "iso_abbreviation": "J Plast Reconstr Aesthet Surg", "category": "Plastic Surgery"},
        {"name": "Annals of Plastic Surgery", "issn": "0148-7043", "iso_abbreviation": "Ann Plast Surg", "category": "Plastic Surgery"},
        {"name": "Plastic Surgery", "issn": "2292-5503", "iso_abbreviation": "Plast Surg (Oakv)", "category": "Plastic Surgery"},
        {"name": "Journal of Craniofacial Surgery", "issn": "1049-2275", "iso_abbreviation": "J Craniofac Surg", "category": "Plastic Surgery"},
        {"name": "Clinics in Plastic Surgery", "issn": "0094-1298", "iso_abbreviation": "Clin Plast Surg", "category": "Plastic Surgery"},
        {"name": "Burns", "issn": "0305-4179", "iso_abbreviation": "Burns", "category": "Plastic Surgery"},
        {"name": "Microsurgery", "issn": "0738-1085", "iso_abbreviation": "Microsurgery", "category": "Plastic Surgery"},
        {"name": "Journal of Reconstructive Microsurgery", "issn": "0743-684X", "iso_abbreviation": "J Reconstr Microsurg", "category": "Plastic Surgery"},
        {"name": "Facial Plastic Surgery Clinics of North America", "issn": "1064-7406", "iso_abbreviation": "Facial Plast Surg Clin North Am", "category": "Plastic Surgery"},
        {"name": "Archives of Plastic Surgery", "issn": "2234-6163", "iso_abbreviation": "Arch Plast Surg", "category": "Plastic Surgery"},
        {"name": "Aesthetic Plastic Surgery", "issn": "0364-216X", "iso_abbreviation": "Aesthetic Plast Surg", "category": "Plastic Surgery"},
        {"name": "Journal of Hand Surgery (American)", "issn": "0363-5023", "iso_abbreviation": "J Hand Surg Am", "category": "Plastic Surgery"},
        {"name": "Journal of Hand Surgery (European)", "issn": "1753-1934", "iso_abbreviation": "J Hand Surg Eur Vol", "category": "Plastic Surgery"},
        {"name": "Cleft Palate-Craniofacial Journal", "issn": "1055-6656", "iso_abbreviation": "Cleft Palate Craniofac J", "category": "Plastic Surgery"},
        {"name": "Hand", "issn": "1558-9447", "iso_abbreviation": "Hand (N Y)", "category": "Plastic Surgery"},
        {"name": "Seminars in Plastic Surgery", "issn": "1535-2188", "iso_abbreviation": "Semin Plast Surg", "category": "Plastic Surgery"},
        {"name": "Plastic and Reconstructive Surgery - Global Open", "issn": "2169-7574", "iso_abbreviation": "Plast Reconstr Surg Glob Open", "category": "Plastic Surgery"},

        # --- Obstetrics and Gynecology ---
        {"name": "Obstetrics & Gynecology (The Green Journal)", "issn": "0029-7844", "iso_abbreviation": "Obstet Gynecol", "category": "OB/GYN"},
        {"name": "American Journal of Obstetrics and Gynecology", "issn": "0002-9378", "iso_abbreviation": "Am J Obstet Gynecol", "category": "OB/GYN"},
        {"name": "Human Reproduction Update", "issn": "1355-4786", "iso_abbreviation": "Hum Reprod Update", "category": "OB/GYN"},
        {"name": "Human Reproduction", "issn": "0268-1161", "iso_abbreviation": "Hum Reprod", "category": "OB/GYN"},
        {"name": "Ultrasound in Obstetrics & Gynecology", "issn": "0960-7692", "iso_abbreviation": "Ultrasound Obstet Gynecol", "category": "OB/GYN"},
        {"name": "BJOG: An International Journal of Obstetrics & Gynaecology", "issn": "1470-0328", "iso_abbreviation": "BJOG", "category": "OB/GYN"},
        {"name": "Fertility and Sterility", "issn": "0015-0282", "iso_abbreviation": "Fertil Steril", "category": "OB/GYN"},
        {"name": "Gynecologic Oncology", "issn": "0090-8258", "iso_abbreviation": "Gynecol Oncol", "category": "OB/GYN"},
        {"name": "Journal of Minimally Invasive Gynecology", "issn": "1553-4650", "iso_abbreviation": "J Minim Invasive Gynecol", "category": "OB/GYN"},
        {"name": "Menopause", "issn": "1072-3714", "iso_abbreviation": "Menopause", "category": "OB/GYN"},
        {"name": "International Journal of Gynecology & Obstetrics", "issn": "0020-7292", "iso_abbreviation": "Int J Gynaecol Obstet", "category": "OB/GYN"},
        {"name": "Contraception", "issn": "0010-7824", "iso_abbreviation": "Contraception", "category": "OB/GYN"},
        {"name": "Paediatric and Perinatal Epidemiology", "issn": "0269-5022", "iso_abbreviation": "Paediatr Perinat Epidemiol", "category": "OB/GYN"},
        {"name": "Placenta", "issn": "0143-4004", "iso_abbreviation": "Placenta", "category": "OB/GYN"},
        {"name": "Journal of Assisted Reproduction and Genetics", "issn": "1058-0468", "iso_abbreviation": "J Assist Reprod Genet", "category": "OB/GYN"},
        {"name": "European Journal of Obstetrics & Gynecology and Reproductive Biology", "issn": "0301-2115", "iso_abbreviation": "Eur J Obstet Gynecol Reprod Biol", "category": "OB/GYN"},
        {"name": "Archives of Gynecology and Obstetrics", "issn": "0932-0067", "iso_abbreviation": "Arch Gynecol Obstet", "category": "OB/GYN"},
        {"name": "BMC Pregnancy and Childbirth", "issn": "1471-2393", "iso_abbreviation": "BMC Pregnancy Childbirth", "category": "OB/GYN"},
        {"name": "Maturitas", "issn": "0378-5122", "iso_abbreviation": "Maturitas", "category": "OB/GYN"},
        {"name": "Prenatal Diagnosis", "issn": "0197-3851", "iso_abbreviation": "Prenat Diagn", "category": "OB/GYN"},

        # --- Gastroenterology and Hepatology ---
        {"name": "Gastroenterology", "issn": "0016-5085", "iso_abbreviation": "Gastroenterology", "category": "Gastroenterology"},
        {"name": "Gut", "issn": "0017-5749", "iso_abbreviation": "Gut", "category": "Gastroenterology"},
        {"name": "Journal of Hepatology", "issn": "0168-8278", "iso_abbreviation": "J Hepatol", "category": "Gastroenterology"},
        {"name": "Nature Reviews Gastroenterology & Hepatology", "issn": "1759-5045", "iso_abbreviation": "Nat Rev Gastroenterol Hepatol", "category": "Gastroenterology"},
        {"name": "Hepatology", "issn": "0270-9139", "iso_abbreviation": "Hepatology", "category": "Gastroenterology"},
        {"name": "American Journal of Gastroenterology", "issn": "0002-9270", "iso_abbreviation": "Am J Gastroenterol", "category": "Gastroenterology"},
        {"name": "Clinical Gastroenterology and Hepatology", "issn": "1542-3565", "iso_abbreviation": "Clin Gastroenterol Hepatol", "category": "Gastroenterology"},
        {"name": "Endoscopy", "issn": "0013-726X", "iso_abbreviation": "Endoscopy", "category": "Gastroenterology"},
        {"name": "Gastrointestinal Endoscopy", "issn": "0016-5107", "iso_abbreviation": "Gastrointest Endosc", "category": "Gastroenterology"},
        {"name": "Alimentary Pharmacology & Therapeutics", "issn": "0269-2813", "iso_abbreviation": "Aliment Pharmacol Ther", "category": "Gastroenterology"},
        {"name": "Journal of Crohn's and Colitis", "issn": "1873-9946", "iso_abbreviation": "J Crohns Colitis", "category": "Gastroenterology"},
        {"name": "Inflammatory Bowel Diseases", "issn": "1078-0998", "iso_abbreviation": "Inflamm Bowel Dis", "category": "Gastroenterology"},
        {"name": "Liver International", "issn": "1478-3223", "iso_abbreviation": "Liver Int", "category": "Gastroenterology"},
        {"name": "Seminars in Liver Disease", "issn": "0272-8087", "iso_abbreviation": "Semin Liver Dis", "category": "Gastroenterology"},
        {"name": "Journal of Viral Hepatitis", "issn": "1352-0504", "iso_abbreviation": "J Viral Hepat", "category": "Gastroenterology"},
        {"name": "Neurogastroenterology and Motility", "issn": "1350-1925", "iso_abbreviation": "Neurogastroenterol Motil", "category": "Gastroenterology"},
        {"name": "Digestion", "issn": "0012-2823", "iso_abbreviation": "Digestion", "category": "Gastroenterology"},
        {"name": "Pancreatology", "issn": "1424-3903", "iso_abbreviation": "Pancreatology", "category": "Gastroenterology"},
        {"name": "Journal of Gastroenterology", "issn": "0944-1174", "iso_abbreviation": "J Gastroenterol", "category": "Gastroenterology"},
        {"name": "United European Gastroenterology Journal", "issn": "2050-6406", "iso_abbreviation": "United European Gastroenterol J", "category": "Gastroenterology"},

        # --- Dermatology ---
        {"name": "Journal of the American Academy of Dermatology", "issn": "0190-9622", "iso_abbreviation": "J Am Acad Dermatol", "category": "Dermatology"},
        {"name": "JAMA Dermatology", "issn": "2168-6068", "iso_abbreviation": "JAMA Dermatol", "category": "Dermatology"},
        {"name": "British Journal of Dermatology", "issn": "0007-0963", "iso_abbreviation": "Br J Dermatol", "category": "Dermatology"},
        {"name": "Journal of Investigative Dermatology", "issn": "0022-202X", "iso_abbreviation": "J Invest Dermatol", "category": "Dermatology"},
        {"name": "Dermatologic Surgery", "issn": "1076-0512", "iso_abbreviation": "Dermatol Surg", "category": "Dermatology"},
        {"name": "JEADV (Journal of the European Academy of Dermatology and Venereology)", "issn": "0926-9959", "iso_abbreviation": "J Eur Acad Dermatol Venereol", "category": "Dermatology"},
        {"name": "American Journal of Clinical Dermatology", "issn": "1175-0561", "iso_abbreviation": "Am J Clin Dermatol", "category": "Dermatology"},
        {"name": "Journal of Dermatological Science", "issn": "0923-1811", "iso_abbreviation": "J Dermatol Sci", "category": "Dermatology"},
        {"name": "Experimental Dermatology", "issn": "0906-6705", "iso_abbreviation": "Exp Dermatol", "category": "Dermatology"},
        {"name": "Contact Dermatitis", "issn": "0105-1873", "iso_abbreviation": "Contact Dermatitis", "category": "Dermatology"},
        {"name": "Pediatric Dermatology", "issn": "0736-8046", "iso_abbreviation": "Pediatr Dermatol", "category": "Dermatology"},
        {"name": "Melanoma Research", "issn": "0960-8931", "iso_abbreviation": "Melanoma Res", "category": "Dermatology"},
        {"name": "Journal of Dermatology", "issn": "0385-2407", "iso_abbreviation": "J Dermatol", "category": "Dermatology"},
        {"name": "Acta Dermato-Venereologica", "issn": "0001-5555", "iso_abbreviation": "Acta Derm Venereol", "category": "Dermatology"},
        {"name": "Clinical and Experimental Dermatology", "issn": "0307-6938", "iso_abbreviation": "Clin Exp Dermatol", "category": "Dermatology"},
        {"name": "Dermatitis", "issn": "1710-3568", "iso_abbreviation": "Dermatitis", "category": "Dermatology"},
        {"name": "Journal of Cutaneous Pathology", "issn": "0303-6987", "iso_abbreviation": "J Cutan Pathol", "category": "Dermatology"},
        {"name": "Australasian Journal of Dermatology", "issn": "0004-8380", "iso_abbreviation": "Australas J Dermatol", "category": "Dermatology"},
        {"name": "International Journal of Dermatology", "issn": "0011-9059", "iso_abbreviation": "Int J Dermatol", "category": "Dermatology"},
        {"name": "Seminars in Cutaneous Medicine and Surgery", "issn": "1085-5629", "iso_abbreviation": "Semin Cutan Med Surg", "category": "Dermatology"},
    ]
    
    async with async_session() as session:
        # Fetch existing journals to create an ISSN map
        stmt = select(Journal)
        existing_result = await session.execute(stmt)
        existing_journals = existing_result.scalars().all()
        # Map ISSN -> Journal object
        existing_map = {j.issn: j for j in existing_journals if j.issn}
        
        seen_issns = set()
        processed_count = 0
        
        for j_data in JOURNALS:
            issn = j_data["issn"]
            # Deduplicate within the seed list
            if issn in seen_issns:
                continue
            seen_issns.add(issn)
            
            if issn in existing_map:
                # Update existing journal (metadata only)
                journal = existing_map[issn]
                journal.name = j_data["name"]
                journal.iso_abbreviation = j_data["iso_abbreviation"]
                journal.category = j_data["category"]
                # We do NOT change the ID, preserving foreign keys
            else:
                # Insert new journal
                new_journal = Journal(**j_data)
                session.add(new_journal)
            
            processed_count += 1
        
        await session.commit()
    
    return {"message": "Seeded successfully (Safe Upsert)", "count": processed_count}
