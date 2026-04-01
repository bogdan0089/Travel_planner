# Travel Planner API

REST API for managing travel projects and places using the [Art Institute of Chicago API](https://api.artic.edu/docs/).

## Stack

- **FastAPI** + async SQLAlchemy + Alembic
- **SQLite** (default) or PostgreSQL via `DATABASE_URL`
- **Redis** — caches Art Institute API responses (1 hour TTL)
- **JWT** — bearer token authentication
- **Docker** + docker-compose

## Quick Start (local)

```bash
# 1. Clone & create virtualenv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env if needed (optional — defaults work out of the box)

# 4. Run
python main.py
```

API available at http://localhost:8000  
Swagger docs at http://localhost:8000/docs

## Docker

```bash
docker-compose up --build
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./travel_planner.db` | SQLAlchemy async DB URL |
| `SECRET_KEY` | `change-me-...` | JWT signing key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token TTL (minutes) |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis URL. Set empty to disable cache |

## API Endpoints

### Auth
| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get JWT token |
| GET | `/auth/me` | Current user info |

### Projects
| Method | Path | Description |
|---|---|---|
| POST | `/projects` | Create project (with optional places) |
| GET | `/projects` | List projects (pagination + status filter) |
| GET | `/projects/{id}` | Get project with places |
| PATCH | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project (blocked if any place visited) |

### Places
| Method | Path | Description |
|---|---|---|
| POST | `/projects/{id}/places` | Add place (validated against Art Institute API) |
| GET | `/projects/{id}/places` | List places (paginated) |
| GET | `/projects/{id}/places/{place_id}` | Get single place |
| PATCH | `/projects/{id}/places/{place_id}` | Update notes / mark visited |

## Business Rules

- Max **10 places** per project
- Same place cannot be added to the same project twice
- Project auto-completes when **all places are visited**
- Project **cannot be deleted** if any place is already visited

## Running Tests

```bash
pytest tests/ -v
```

## API Documentation

**Swagger UI** (interactive): http://localhost:8000/docs  
**OpenAPI JSON**: http://localhost:8000/openapi.json

## Postman Collection

Import `Travel_Planner.postman_collection.json` from the repo root into Postman.

Workflow:
1. Run **Register** → **Login** (token is saved automatically to `{{token}}` variable)
2. Run **Create project** (project_id saved to `{{project_id}}`)
3. Run **Add place** (place_id saved to `{{place_id}}`)
4. Use **Update / Mark visited** requests
