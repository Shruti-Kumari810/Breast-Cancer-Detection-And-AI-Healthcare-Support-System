from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.resource import HealthResourceOut
from app.services.directory_service import DirectoryService

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[HealthResourceOut])
def get_resources(resource_type: str | None = None, db: Session = Depends(get_db)):
    return DirectoryService(db).resources(resource_type)

