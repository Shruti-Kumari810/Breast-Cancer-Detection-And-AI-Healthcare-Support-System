# Phase 1 - Project Structure

## Goal

Create the top-level production project scaffold for the AI-Powered Breast Cancer Detection and Healthcare Support System.

## Architecture Overview

The project is separated into clear application layers:

- **Frontend layer**: Streamlit application for web and mobile-friendly user experiences.
- **Backend layer**: FastAPI service exposing secure REST APIs.
- **Machine learning layer**: Data preparation, model training, model comparison, saved models, and explainability assets.
- **Database layer**: PostgreSQL schema, SQLAlchemy ORM models, and Alembic migrations.
- **Reporting layer**: Generated PDF reports and report templates.
- **Documentation layer**: Architecture, installation, API, deployment, user manual, ER diagram, data flow diagram, and system design documents.
- **Testing layer**: Unit tests, API tests, and model validation tests.
- **Deployment layer**: Docker, Docker Compose, environment templates, and cloud deployment notes.

## Folder Responsibilities

### backend/

Contains the FastAPI application. This will include API routers, controllers, services, dependency injection, authentication, JWT handling, Pydantic schemas, configuration, and backend application startup code.

Expected future structure:

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
└── requirements.txt
```

### frontend/

Contains the Streamlit application, custom HTML/CSS, Bootstrap-enhanced UI components, Plotly charts, reusable page modules, and mobile/PWA assets.

Expected future structure:

```text
frontend/
├── app.py
├── pages/
├── components/
├── assets/
└── requirements.txt
```

### ml_models/

Contains dataset loading scripts, EDA notebooks or scripts, preprocessing pipelines, trained models saved with Joblib, SHAP explainability utilities, model metrics, and model comparison artifacts.

Expected future structure:

```text
ml_models/
├── data/
├── notebooks/
├── scripts/
├── artifacts/
└── reports/
```

### database/

Contains database schema ownership: SQLAlchemy database setup, Alembic migration configuration, migration versions, seed data, and raw SQL schema references.

Expected future structure:

```text
database/
├── alembic/
├── migrations/
├── seeds/
└── schema.sql
```

### reports/

Contains generated PDF reports, report templates, and report generation utilities. Patient prediction reports will include patient details, prediction result, confidence score, selected model, and recommended doctors.

### docs/

Contains human-facing and engineering documentation, including API documentation, installation guide, user manual, architecture diagram, ER diagram, data flow diagram, and system design document.

### tests/

Contains Pytest-based test suites for backend APIs, services, machine learning code, database interactions, and frontend-safe utility functions.

Expected future structure:

```text
tests/
├── unit/
├── api/
├── model/
└── conftest.py
```

### docker/

Contains Dockerfiles and Docker-specific runtime assets for backend and frontend services.

### deployment/

Contains production deployment instructions and configuration examples for Render or Railway, Streamlit Cloud, PostgreSQL hosting, environment variables, and one-command deployment.

## Confirmation Gate

Phase 1 is complete once the scaffold exists and the folder responsibilities are documented. The next phase should begin only after confirmation.

