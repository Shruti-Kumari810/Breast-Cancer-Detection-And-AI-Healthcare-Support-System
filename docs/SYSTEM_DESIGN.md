# System Design Document

## Architecture

The system uses a separated frontend-backend architecture.

- Streamlit provides responsive web and mobile-friendly UI.
- FastAPI exposes secure REST APIs.
- PostgreSQL stores patients, predictions, doctors, appointments, resources, and users.
- SQLAlchemy manages ORM mapping.
- Alembic manages schema migrations.
- Scikit-learn trains Logistic Regression, SVM, and Random Forest models.
- Joblib persists model artifacts.
- Plotly renders dashboard and explainability charts.
- ReportLab generates PDF reports.

## Data Flow

1. Doctor logs in and receives JWT.
2. Doctor creates or selects patient.
3. UI sends diagnostic measurements to FastAPI.
4. Prediction service loads selected Joblib model.
5. Model returns class probability and confidence.
6. Prediction is saved to PostgreSQL when a patient ID is provided.
7. UI displays result, feature contributions, reports, doctors, and analytics.

## Security

- JWT bearer authentication protects clinical endpoints.
- Passwords are hashed using bcrypt.
- CORS is environment-configurable.
- Production deployments must override `SECRET_KEY`.

## Model Governance

- All three algorithms are evaluated with train-test split, stratified cross-validation, GridSearchCV, and ROC-AUC comparison.
- The best model is selected by ROC-AUC.
- Feature contribution display supports interpretability for clinical review.

