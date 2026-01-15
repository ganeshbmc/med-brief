# Session Progress: 2026-01-14 - Docker Connectivity Fix

## Summary
Fixed backend connectivity in GitHub Codespaces by configuring Docker Compose networking correctly.

## Problem
- Frontend container couldn't reach backend container
- API requests returned `{"detail":"Not Found"}`
- `VITE_API_URL=http://localhost:8000` was incorrect inside Docker

## Changes Made

### 1. Created `frontend/.env.local`
```
VITE_API_URL=http://localhost:8000
```
- Used by local development (restart-dev.sh)
- Vite proxy handles routing in local dev

### 2. Created `docker-compose.override.yml`
```yaml
services:
  frontend:
    environment:
      - VITE_API_URL=http://backend:8000
```
- Override for Codespaces
- Uses Docker's internal DNS to reach backend

### 3. Updated `docker-compose.yml`
- Removed obsolete `version: "3.9"` field
- Changed `VITE_API_URL` to `http://backend:8000`

## Configuration Matrix
| Environment | API URL | Method |
|------------|---------|--------|
| Local dev | localhost:8000 | Vite proxy |
| Codespaces | backend:8000 | Docker DNS |
| Railway | Same origin | Static files |

## Action Taken
- Seeded database with preset journals (Medicine, Cardiology, Oncology)
- `POST /seed` returned successful upsert

## Commands Executed
```bash
docker-compose down && docker-compose up -d
curl -X POST http://localhost:8000/seed
```

## Files Changed
- `frontend/.env.local` (new)
- `docker-compose.override.yml` (new)
- `docker-compose.yml` (modified)
