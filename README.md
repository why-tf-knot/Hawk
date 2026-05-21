# Hawk — Industrial Emissions Monitoring (Starter)

Hawk is a modular full-stack GIS web app starter for industrial aerosol and emissions monitoring:
- **Frontend**: React + TypeScript + Vite + Leaflet
- **Middleware/API**: FastAPI with typed models and modular services
- **Geospatial processing backend**: Earth Engine service wrapper with mock mode and production-ready extension points

## Monorepo structure

- `/backend` FastAPI API layer
  - `app/api/routes.py` endpoints
  - `app/models/schemas.py` typed request/response models
  - `app/services/*` modular services
  - `app/services/earth_engine_service.py` reusable Earth Engine workflow functions
- `/frontend` React app with component-based layout
  - left control panel, map canvas, bottom trend panel

## Backend endpoints

Implemented:
- `GET /health`
- `GET /cities/search?q=`
- `POST /analysis/city`
- `GET /analysis/{job_id}/status`
- `GET /analysis/{job_id}/summary`
- `GET /analysis/{job_id}/polygons`
- `GET /analysis/{job_id}/timeseries?site_id=`
- `GET /analysis/{job_id}/tiles/{layer_name}`
- `GET /analysis/{job_id}/legend/{layer_name}`
- `POST /exports/report`
- `POST /exports/geojson`
- `POST /exports/csv`
- `POST /exports/timelapse`

## Scientific integrity guardrails

The implementation enforces scale-aware interpretation:
- Sentinel-2/Sentinel-1 are used for surface industrial mapping (fine scale)
- Sentinel-5P atmospheric products are represented at coarse native resolution and for zone-level interpretation only
- outputs include resolution and quality metadata
- temporal coverage years are returned in analysis summary for multi-year evolution views
- attribution is confidence-scored and probabilistic, not deterministic

## Environment configuration

Copy and adapt:

```bash
cp backend/.env.example backend/.env
```

`backend/.env.example`:
- `MOCK_MODE` default true for local development without live Earth Engine credentials
- `EARTH_ENGINE_PROJECT` for production Earth Engine execution
- optional cache/database fields (`REDIS_URL`, `DATABASE_URL`)

## Local development

### Backend

```bash
cd backend
pip install -e .[test]
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker compose up --build
```

## Testing

```bash
cd backend
pytest
```

## Earth Engine authentication (production)

1. Install Earth Engine Python API and authenticate service account or user credentials.
2. Set `EARTH_ENGINE_PROJECT` in backend `.env`.
3. Extend `earth_engine_service.py` mock implementations with authenticated `ee` calls.

## Module-by-module extension plan

1. Harden geocoding provider integration and AOI retrieval
2. Wire real Earth Engine preprocessing and feature extraction functions
3. Add model training/inference for industrial classification and emissions relevance
4. Add persistent cache (Redis) and PostGIS storage
5. Expand export generation into downloadable artifacts

## Current mock/demo support

- Seed city examples included for local operation
- Analysis pipeline returns deterministic demo polygons, zone stats, tiles, and time series
- TODO markers included where model thresholds should be tuned
