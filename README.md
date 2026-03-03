# UOP API

FastAPI backend for the Unified Observability Portal. Serves all dashboard, graph, announcements, teams, notifications, and AURA chat endpoints.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

The API runs at `http://localhost:8080`. Verify with `curl http://localhost:8080/`.

## Project Structure

```
app/
  main.py            # FastAPI app, CORS, router registration
  config.py          # Environment variables (USE_MOCK_DATA, SMTP, DB, CORS)
  schemas.py         # Pydantic request models
  routers/           # Endpoint modules (dashboard, applications, graph, etc.)
  services/          # Business logic (enrichment, graph engine, email, VC monitor)
  mock_data/         # Static seed data for demo mode
docs/                # API specifications and architecture docs
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `USE_MOCK_DATA` | `true` | Use in-memory mock data (set `false` for real APIs) |
| `DATABASE_URL` | ` ` | MySQL connection string (e.g. `mysql+pymysql://user:pass@host/db`) |
| `SMTP_HOST` | ` ` | SMTP server for email notifications |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USER` | ` ` | SMTP username |
| `SMTP_PASSWORD` | ` ` | SMTP password |
| `SMTP_FROM` | `uop-api@example.com` | Sender email address |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins |
| `LOG_LEVEL` | `INFO` | Python logging level |

## Cloud Foundry Deployment

```bash
cf push
```

Uses `manifest.yml` with `python_buildpack`. Health check on `/api/health-summary`.

## Wiring Real APIs

Each `mock_data/` module has `# REAL: Replace with <service> call` comments showing what to swap out. The general pattern:

1. Set `USE_MOCK_DATA=false`
2. Set `DATABASE_URL` to your MySQL instance
3. Replace mock data imports in services with actual API calls or SQLAlchemy queries
4. The `config.py` already has `DATABASE_URL` ready for `sqlalchemy` integration

### MySQL + SQLAlchemy

Add to `requirements.txt`:
```
sqlalchemy
pymysql
```

Create `app/database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

## API Documentation

See [docs/API-CURRENT.md](docs/API-CURRENT.md) for endpoint reference and [docs/API_DATA.md](docs/API_DATA.md) for data specifications.
