from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.doctor import DoctorOut
from app.services.directory_service import DirectoryService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[DoctorOut])
def list_doctors(
    city: str | None = None,
    specialization: str | None = None,
    db: Session = Depends(get_db),
):
    return DirectoryService(db).doctors(city, specialization)


@router.get("/{doctor_id}", response_model=DoctorOut)
def doctor_details(doctor_id: int, db: Session = Depends(get_db)):
    doctor = DirectoryService(db).doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

