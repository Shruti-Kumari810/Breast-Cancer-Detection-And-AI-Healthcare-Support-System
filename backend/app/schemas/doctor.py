from pydantic import BaseModel


class DoctorOut(BaseModel):
    doctor_id: int
    doctor_name: str
    specialization: str
    hospital_name: str
    city: str
    experience: int
    contact: str

    model_config = {"from_attributes": True}

