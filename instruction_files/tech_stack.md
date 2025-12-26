# Tech Stack

## Backend
- **Language**: Python 3.10+
- **Framework**: FastAPI (Async)
- **Database**: 
  - ORM: SQLAlchemy (Async)
  - Migrations: Alembic
  - RDBMS: SQLite (Dev) / PostgreSQL (Prod)
- **External APIs**: PubMed Entrez API (via BioPython or httpx)
- **Testing**: Pytest

## Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **Styling**: Bootstrap 5
- **State Management**: Pinia
- **Testing**: Vitest (optional for v1)

## DevOps / Infrastructure
- **Containerization**: Docker (Multi-stage builds)
- **Orchestration**: Docker Compose (Local Dev)
- **Production**: Cloud Run (target)
- **CI/CD**: GitHub Actions (future)
