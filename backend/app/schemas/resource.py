from pydantic import BaseModel


class HealthResourceOut(BaseModel):
    resource_id: int
    title: str
    description: str
    resource_type: str
    url: str

    model_config = {"from_attributes": True}

