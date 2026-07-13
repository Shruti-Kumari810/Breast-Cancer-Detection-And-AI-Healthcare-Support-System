# Installation Guide

## Local Setup

Use Python 3.11 or 3.12. The scientific stack used by Pandas, NumPy, and Scikit-learn may not publish wheels for very new Python versions immediately.

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

On Windows PowerShell:

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

Frontend: `http://localhost:8501`

Backend: `http://localhost:8000/docs`
