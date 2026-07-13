from datetime import datetime

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime


class AppointmentOut(AppointmentCreate):
    appointment_id: int
    status: str

    model_config = {"from_attributes": True}

