from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class PatientBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=0, le=120)
    phone: str
    email: EmailStr
    address: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, ge=0, le=120)
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class PatientOut(PatientBase):
    patient_id: int
    created_at: datetime

    model_config = {"from_attributes": True}

