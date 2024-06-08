from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum as pyEnum

class EntityType(str, pyEnum):
    Internal = "Internal"
    Government = "Government"
    Company = "Company"

class EnvironmentType(str, pyEnum):
    Development = "Development"
    Staging = "Staging"
    Production = "Production"

class Contact(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True, nullable=False)
    name: str = Field(index=True)
    email: str = Field(index=True)
    mobile_number: Optional[str] = None
    office_number: Optional[str] = None
    entity_id: int = Field(foreign_key="entity.id")
    entity: "Entity" = Relationship(back_populates="contacts")

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

class Entity(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name_en: str = Field(index=True)
    name_arb: str = ""
    ABBR: str = ""
    entity_type: EntityType = Field(sa_column=pyEnum(EntityType))
    contacts: List["Contact"] = Relationship(back_populates="entity")
    #ports: List["Port"] = Relationship(back_populates="entity")

    consumer_certificates: List["Certificate"] = Relationship(back_populates="consumer_entity")
    user_accounts: List["UserAccount"] = Relationship(back_populates="entity")

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

class Environment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = ""
    ip_address: str = ""
    environment_type: EnvironmentType = Field(sa_column=pyEnum(EnvironmentType)) 
    ports: List["Port"] = Relationship(back_populates="entity")

class Port(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    number: int = 0
    environment_id: int = Field(foreign_key="environment.id")
    environment: "Environment" = Relationship(back_populates="ports")
    service_access: str = ""
    allowed_access: str = ""

    entity_id: int = Field(foreign_key="entity.id")
    entity: "Entity" = Relationship(back_populates="ports")

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

class UserAccount(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    roles: str = ""
    entity_id: int = Field(foreign_key="entity.id")
    entity: "Entity" = Relationship(back_populates="user_accounts")
    certificates: List["Certificate"] = Relationship(back_populates="user_account")

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

class Certificate(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)
    serial_number: str = Field(index=True)
    issuer_name: str = Field(index=True)
    subject_name: str = Field(index=True)
    expiry_date: str = ""
    entity_id: int = Field(foreign_key="entity.id")
    entity: "Entity" = Relationship(back_populates="certificates")
    consumer_entity_id: int = Field(foreign_key="entity.id")
    consumer_entity: "Entity" = Relationship(back_populates="consumer_certificates")
    user_account_id: int = Field(foreign_key="user_account.id")
    user_account: "UserAccount" = Relationship(back_populates="certificates")

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})