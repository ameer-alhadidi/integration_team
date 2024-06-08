from typing import Any
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

from  .base_class import IDModelMixin, CoreModel,UserDateTimeModelMixin


class ContactBase(CoreModel):
    """
    Contact base model for the rest response
    """
    name: str
    email: EmailStr
    office_number: str = Field( 
        title="Office number", 
        description= "Office number has to be of length 8",
        max_length=14, 
        pattern='^\\d{8}$',
        alias= "office_number",
    )
    mobile_number: str
    entity_id:int
    
    
    class Config:
        from_attributes = True

class ContactListOut(CoreModel):
    contacts: list[ContactBase] | None = None,

    class Config:
        from_attributes = True

class ContactOut(ContactBase):
    pass
    class Config:
        from_attributes = True

class ContactCreate(ContactBase):
    pass
    class Config:
        from_attributes = True

class ContactUpdate(ContactBase,UserDateTimeModelMixin,IDModelMixin):
    pass
    class Config:
        from_attributes = True

class Contact(ContactBase,IDModelMixin):
    pass
    class Config:
        from_attributes = True

class ContactAdmin(Contact,UserDateTimeModelMixin):
    pass