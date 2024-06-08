from pydantic import BaseModel,field_validator
from datetime import datetime
from typing import Optional


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here. e.g. created, updated
    """
    pass

class IDModelMixin(BaseModel):
    id: int
    
class StatusModel(BaseModel):
    code: str
    description_en: str
    description_ar: str

class ResponseModel(BaseModel):
    data: dict
    status: StatusModel

class UserDateTimeModelMixin(BaseModel):
    created_by: str
    created_at: Optional[datetime]
    updated_by: str
    updated_at: Optional[datetime]
    
    @field_validator("created_at", "updated_at")
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()
