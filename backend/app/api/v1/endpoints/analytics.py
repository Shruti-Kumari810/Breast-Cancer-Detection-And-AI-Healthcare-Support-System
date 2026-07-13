from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.patient import Patient
from app.models.prediction import Prediction

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total_patients = db.query(Patient).count()
    total_predictions = db.query(Prediction).count()
    benign_cases = db.query(Prediction).filter(Prediction.prediction_result == "Benign").count()
    malignant_cases = db.query(Prediction).filter(Prediction.prediction_result == "Malignant").count()
    rows = db.query(Prediction).all()
    algorithm_comparison: dict[str, int] = {}
    monthly: dict[str, int] = {}
    for row in rows:
        algorithm_comparison[row.algorithm_used] = algorithm_comparison.get(row.algorithm_used, 0) + 1
        month = row.prediction_date.strftime("%Y-%m")
        monthly[month] = monthly.get(month, 0) + 1
    return {
        "total_patients": total_patients,
        "total_predictions": total_predictions,
        "benign_cases": benign_cases,
        "malignant_cases": malignant_cases,
        "algorithm_comparison": algorithm_comparison,
        "monthly_trends": monthly,
    }
