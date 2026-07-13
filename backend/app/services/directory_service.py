from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.resource import HealthResource
from app.schemas.appointment import AppointmentCreate


class DirectoryService:
    def __init__(self, db: Session):
        self.db = db

    def doctors(self, city: str | None = None, specialization: str | None = None) -> list[Doctor]:
        query = self.db.query(Doctor)
        if city:
            query = query.filter(Doctor.city.ilike(f"%{city}%"))
        if specialization:
            query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
        return query.order_by(Doctor.experience.desc()).all()

    def doctor(self, doctor_id: int) -> Doctor | None:
        return self.db.get(Doctor, doctor_id)

    def book(self, payload: AppointmentCreate) -> Appointment:
        appointment = Appointment(**payload.model_dump(), status="booked")
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def cancel(self, appointment_id: int) -> Appointment | None:
        appointment = self.db.get(Appointment, appointment_id)
        if appointment:
            appointment.status = "cancelled"
            self.db.commit()
            self.db.refresh(appointment)
        return appointment

    def resources(self, resource_type: str | None = None) -> list[HealthResource]:
        query = self.db.query(HealthResource)
        if resource_type:
            query = query.filter(HealthResource.resource_type == resource_type)
        return query.order_by(HealthResource.title).all()

