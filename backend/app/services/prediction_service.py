from sqlalchemy.orm import Session

from app.ml.prediction_engine import prediction_engine
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionRequest


class PredictionService:
    def __init__(self, db: Session):
        self.db = db

    def predict(self, payload: PredictionRequest) -> dict:
        result = prediction_engine.predict(payload.features, payload.algorithm)
        prediction_id = None
        if payload.patient_id:
            record = Prediction(
                patient_id=payload.patient_id,
                algorithm_used=result["selected_model"],
                prediction_result=result["prediction_result"],
                confidence_score=result["confidence_score"],
            )
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            prediction_id = record.prediction_id
        return {"prediction_id": prediction_id, **result}

    def history(self, patient_id: int | None = None) -> list[Prediction]:
        query = self.db.query(Prediction)
        if patient_id:
            query = query.filter(Prediction.patient_id == patient_id)
        return query.order_by(Prediction.prediction_date.desc()).all()

