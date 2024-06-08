
from typing import List
from click import DateTime
from pydantic import BaseModel
 
class ContactBase(BaseModel):
    name: str
    email: str
    contactNumber: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class ContactAdmin(Contact):
    created_by: str
    created_at: DateTime
    updated_by: str
    updated_at: DateTime

class PortBase(BaseModel):
    number: int
    service_access: str
    allowed_access: str

class PortCreate(PortBase):
    pass

class Port(PortBase):
    id: int

    class Config:
        orm_mode = True

class PortAdmin(Port):
    created_by: str
    created_at: DateTime
    updated_by: str
    updated_at: DateTime

class CertificateBase(BaseModel):
    name: str
    expiry_date: str

class CertificateCreate(CertificateBase):
    pass

class Certificate(CertificateBase):
    id: int

    class Config:
        orm_mode = True

class CertificateAdmin(Certificate):
    created_by: str
    created_at: DateTime
    updated_by: str
    updated_at: DateTime

class UserAccountBase(BaseModel):
    name: str
    roles: List[str]

class UserAccountCreate(UserAccountBase):
    pass

class UserAccount(UserAccountBase):
    id: int
    certificates: List[Certificate] = []

    class Config:
        orm_mode = True

class UserAccountAdmin(UserAccount):
    created_by: str
    created_at: DateTime
    updated_by: str
    updated_at: DateTime

class EntityBase(BaseModel):
    name: str
    name_arb: str
    ABBR: str
    entity_type: str
    environment: str

class EntityCreate(EntityBase):
    contacts: List[ContactCreate] = []
    ports: List[PortCreate] = []
    certificates: List[CertificateCreate] = []
    consumer_certificates: List[CertificateCreate] = []
    user_accounts: List[UserAccountCreate] = []

class Entity(EntityBase):
    id: int
    contacts: List[Contact] = []
    ports: List[Port] = []
    certificates: List[Certificate] = []
    consumer_certificates: List[Certificate] = []
    user_accounts: List[UserAccount] = []

    class Config:
        orm_mode = True

class EntityAdmin(Entity):
    created_by: str
    created_at: DateTime
    updated_by: str
    updated_at: DateTime
    contacts: List[ContactAdmin] = []
    ports: List[PortAdmin] = []
    certificates: List[CertificateAdmin] = []
    consumer_certificates: List[CertificateAdmin] = []
    user_accounts: List[UserAccountAdmin] = []