from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database import Base

# SQLAlchemy models
class ContactModel(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    contactNumber = Column(String)
    # entity_id = Column(Integer, ForeignKey("entities.id"))
    # entity = relationship("EntityModel", back_populates="contacts")
    created_by = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_by = Column(String)
    updated_at = Column(DateTime, onupdate=func.now())

class PortModel(Base):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    service_access = Column(String)
    allowed_access = Column(String)
    entity_id = Column(Integer, ForeignKey("entities.id"))
    entity = relationship("Entity", back_populates="ports")
    created_by = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_by = Column(String)
    updated_at = Column(DateTime, onupdate=func.now())

# class CertificateModel(Base):
#     __tablename__ = "certificates"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     expiry_date = Column(String)
#     entity_id = Column(Integer, ForeignKey("entities.id"))
#     entity = relationship("EntityModel", back_populates="certificates")
#     consumer_entity_id = Column(Integer, ForeignKey("entities.id"))
#     consumer_entity = relationship("EntityModel", back_populates="consumer_certificates")
#     user_account_id = Column(Integer, ForeignKey("user_accounts.id"))
#     user_account = relationship("UserAccountModel", back_populates="certificates")
#     created_by = Column(String)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_by = Column(String)
#     updated_at = Column(DateTime, onupdate=func.now())

# class UserAccountModel(Base):
#     __tablename__ = "user_accounts"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     roles = Column(String)
#     entity_id = Column(Integer, ForeignKey("entities.id"))
#     entity = relationship("EntityModel", back_populates="user_accounts")
#     certificates = relationship("CertificateModel", back_populates="user_account")
#     created_by = Column(String)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_by = Column(String)
#     updated_at = Column(DateTime, onupdate=func.now())

# class EntityModel(Base):
#     __tablename__ = "entities"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     name_arb = Column(String)
#     ABBR = Column(String)
#     entity_type = Column(String)
#     environment = Column(String)
#     contacts = relationship("ContactModel", back_populates="entity")
#     ports = relationship("PortModel", back_populates="entity")
#     certificates = relationship("CertificateModel", back_populates="entity")
#     consumer_certificates = relationship("CertificateModel", back_populates="consumer_entity")
#     user_accounts = relationship("UserAccountModel", back_populates="entity")
#     created_by = Column(String)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_by = Column(String)
#     updated_at = Column(DateTime, onupdate=func.now())
