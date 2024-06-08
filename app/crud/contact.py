from sqlalchemy.orm import Session
from icecream import ic
from ..models import models
from ..schemas import contact as schema_contact

def count_contacts(db: Session):
    return db.query(models.Contact).count()

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schema_contact.Contact):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    #ic(db.__dict__)
    return db_contact


def update_contact(db: Session, contact_id: int, contact:  schema_contact.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        for field, value in contact.model_dump(exclude_unset=True).items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact