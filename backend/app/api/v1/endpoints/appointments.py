from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services.directory_service import DirectoryService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("", response_model=AppointmentOut)
def book_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    return DirectoryService(db).book(payload)


@router.post("/{appointment_id}/cancel", response_model=AppointmentOut)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = DirectoryService(db).cancel(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

