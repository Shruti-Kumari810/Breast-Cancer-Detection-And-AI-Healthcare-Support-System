from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class HealthResource(Base):
    __tablename__ = "health_resources"

    resource_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(160))
    description: Mapped[str] = mapped_column(Text)
    resource_type: Mapped[str] = mapped_column(String(80), index=True)
    url: Mapped[str] = mapped_column(String(500))

