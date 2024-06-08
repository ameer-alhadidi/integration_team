from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from app.schemas.base_class import CoreModel

class PortBase(CoreModel):
    number: int
    service_access: str
    allowed_access: str
    entity_id: int
    

class PortCreate(PortBase):
    pass

class PortUpdate(PortBase):
    number: Optional[int] = None
    service_access: Optional[str] = None
    allowed_access: Optional[str] = None
    entity_id: Optional[int] = None

class PortDelete(CoreModel ):
    id: int

class PortOut(PortBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True

class PortListOut(CoreModel):
    ports: List[PortOut]
    total_count: int

    class Config:
        orm_mode = True