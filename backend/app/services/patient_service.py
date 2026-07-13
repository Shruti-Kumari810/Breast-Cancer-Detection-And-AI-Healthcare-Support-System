from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: PatientCreate) -> Patient:
        patient = Patient(**payload.model_dump())
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def list(self) -> list[Patient]:
        return self.db.query(Patient).order_by(Patient.created_at.desc()).all()

    def get(self, patient_id: int) -> Patient:
        patient = self.db.get(Patient, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient

    def update(self, patient_id: int, payload: PatientUpdate) -> Patient:
        patient = self.get(patient_id)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(patient, key, value)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete(self, patient_id: int) -> None:
        patient = self.get(patient_id)
        self.db.delete(patient)
        self.db.commit()

