from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import Field
from app.schemas.base_class import CoreModel, IDModelMixin
from app.schemas.contact import ContactBase


class EntityType(str, Enum):
    Internal = "Internal"
    Government = "Government"
    Company = "Company"

    @staticmethod
    def fetch_names():
        return [c.value for c in EntityType]


class EntityBase(CoreModel,IDModelMixin):
    name_en: str
    name_arb: Optional[str]
    ABBR: Optional[str]
    entity_type: EntityType
    contacts: List[ContactBase] = []
    # created_by: Optional[str]
    # updated_by: Optional[str]
    # created_at: datetime = Field(default_factory=datetime.now)
    # updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class EntityOnlyOut(CoreModel):
    name_en: str
    name_arb: Optional[str]
    ABBR: Optional[str]
    entity_type: EntityType

    class Config:
        from_attributes = True

class EntitiyOnlyListOut(CoreModel):
    entities: list[EntityOnlyOut] | None = None,

    class Config:
        from_attributes = True

class EntitiyListOut(CoreModel):
    entities: list[EntityBase] | None = None,

    class Config:
        from_attributes = True

class EntityCreate(CoreModel):
    name_en: str
    name_arb: Optional[str]
    ABBR: Optional[str]
    entity_type: EntityType
    created_by: Optional[str]
    updated_by: Optional[str]

class EntityUpdate(CoreModel):
    name_en: Optional[str]
    name_arb: Optional[str]
    ABBR: Optional[str]
    entity_type: Optional[EntityType]
    created_by: Optional[str]
    updated_by: Optional[str]

class EntityInDB(EntityBase):
    pass