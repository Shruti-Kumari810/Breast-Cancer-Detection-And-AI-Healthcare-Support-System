from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    doctor_name: Mapped[str] = mapped_column(String(120), index=True)
    specialization: Mapped[str] = mapped_column(String(120), index=True)
    hospital_name: Mapped[str] = mapped_column(String(180))
    city: Mapped[str] = mapped_column(String(120), index=True, default="General")
    experience: Mapped[int] = mapped_column(Integer)
    contact: Mapped[str] = mapped_column(String(80))

    appointments = relationship("Appointment", back_populates="doctor")

