# ?? AI-Powered Breast Cancer Detection & Healthcare Support System

An intelligent healthcare platform that leverages Machine Learning to assist in the early detection of breast cancer while providing patient record management, doctor discovery, appointments, and healthcare support.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green)

## Phase Status

Current status: **Complete working project scaffold with backend, frontend, ML, database, tests, Docker, and documentation.**

## Technology Stack

- Frontend: Streamlit, HTML, CSS, Bootstrap, Plotly, Streamlit Components
- Backend: FastAPI, Python
- Database: PostgreSQL, SQLAlchemy ORM, Alembic
- Machine Learning: Scikit-learn, Pandas, NumPy, Joblib
- Testing: Pytest, FastAPI TestClient
- Deployment: Docker, Docker Compose, Render or Railway, Streamlit Cloud

## Features

- Breast cancer prediction with Logistic Regression, SVM, and Random Forest
- JWT authentication for doctors and clinical users
- Patient registration, update, delete, and history views
- Appointment booking and cancellation
- PDF prediction reports and analytics
- Doctor directory with city and specialization filters
- PostgreSQL schema, SQLAlchemy models, and Alembic migration
- Pytest API, unit, and model tests
- Backend and frontend Dockerfiles plus Docker Compose

## Folder Structure

```text
breast_cancer_detection/
+-- backend/
+-- frontend/
+-- ml_models/
+-- database/
+-- reports/
+-- docs/
+-- tests/
+-- docker/
+-- deployment/
+-- README.md
```

## Quick Start

Recommended runtime: Python 3.11 or 3.12.

```bash
cd breast_cancer_detection
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
python ml_models/scripts/train_models.py
uvicorn app.main:app --app-dir backend --reload
streamlit run frontend/app.py
```

Windows PowerShell:

```powershell
cd breast_cancer_detection
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
pip install -r frontend\requirements.txt
python ml_models\scripts\train_models.py
uvicorn app.main:app --app-dir backend --reload
streamlit run frontend\app.py
```

## Docker

```bash
docker compose up --build
```
## Live Demo 
### 🌐 Frontend (Streamlit)

https://breast-cancer-detection-and-ai-healthcare-support-system-9sjcx.streamlit.app

### ⚙️ Backend API (FastAPI)

https://breast-cancer-detection-and-ai.onrender.com/docs

## Important Medical Disclaimer

This software provides clinical decision support only. It is not a medical diagnosis system and must not replace evaluation by qualified healthcare professionals.
