#codebase

# sightseeings_app

Lightweight FastAPI service for managing sightseeing records (CRUD). Uses SQLAlchemy for persistence and Alembic for schema migrations.

## Features
- REST API for sightseeings (create, read, update, delete)
- SQLAlchemy 2.0 models with Pydantic schemas
- Dependency-injected repository and DB sessions
- Alembic migrations
- Tests with pytest and FastAPI TestClient

## Quickstart

Prerequisites
- Python (recommend 3.11+)
- Virtual environment tool (venv, pipenv, or poetry)
- Install project dependencies (example using pip):

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # or use poetry install if using poetry
```

Note: Project has pyproject.toml; adapt to your preferred workflow (pip/poetry).

Configuration
- Config files are stored in `environments/`
- Default DB URL is in `environments/config.ini` (sqlite by default)
- App reads environment via `src.configuration.config.AppConfig`

Database & migrations
- To create DB schema from models (for development):
  - Run the app once (it creates DB when started) or:
  - Use Alembic:
    - Configure `alembic.ini` or ensure `environments/config.ini` contains the DB URL
    - Run: `alembic upgrade head`

Run the app
- From project root:
```bash
uvicorn src.main:app --reload
# or
python -m src.main
```
- Service exposes routes under `/api/sightseeings`

API Endpoints (HTTP)
- GET /api/sightseeings/           — list items (supports `skip` and `limit`)
- POST /api/sightseeings/          — create item (JSON body: name, location, description)
- GET /api/sightseeings/{id}       — get by id
- PATCH /api/sightseeings/{id}     — partial update (JSON body with any fields)
- DELETE /api/sightseeings/{id}    — delete item

Example create (curl)
```bash
curl -X POST "http://127.0.0.1:8000/api/sightseeings/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Eiffel Tower","location":"Paris","description":"Famous tower"}'
```

Testing
- Tests live in `tests/` and use an in-memory SQLite DB.
- Run tests:
```bash
pytest -q
```

Development notes
- Dependency injection helpers are in `src/dependency_injection/di.py`
- Models are in `src/database/models.py`, Pydantic schemas in `src/schemas/schemas.py`
- Repository layer in `src/repository/sightseeings_repository.py`
- Routes in `src/routes/sightseeings_routes.py`

License
- MIT — see LICENSE file.