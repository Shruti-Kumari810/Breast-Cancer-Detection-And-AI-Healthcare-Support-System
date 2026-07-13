# Deployment Guide

## Backend on Render or Railway

1. Create a PostgreSQL database.
2. Create a web service from this repository.
3. Set root directory to `breast_cancer_detection`.
4. Build command:

```bash
pip install -r backend/requirements.txt && python ml_models/scripts/train_models.py
```

5. Start command:

```bash
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT
```

6. Set environment variables:

```text
DATABASE_URL=postgresql+psycopg://...
SECRET_KEY=<strong-secret>
BACKEND_CORS_ORIGINS=https://your-streamlit-app.streamlit.app
```

## Frontend on Streamlit Cloud

1. Select `frontend/app.py` as the app entrypoint.
2. Add `frontend/requirements.txt`.
3. Set secret/environment:

```text
API_BASE_URL=https://your-backend.example.com/api/v1
```

## One-command Docker Deployment

```bash
docker compose up --build
```
