from sqlalchemy.orm import Session,joinedload
from icecream import ic
from ..models import models
from ..schemas import entity as schema_entity


def get_entity(db: Session, entity_id: int):
    return db.query(models.Entity).options(joinedload(models.Entity.contacts)).filter(models.Entity.id == entity_id).first()

def get_entities_no_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Entity).offset(skip).limit(limit).all()

def get_entities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Entity).options(joinedload(models.Entity.contacts)).offset(skip).limit(limit).all()

def create_entity(db: Session, entity: schema_entity.EntityCreate):
    db_entity = models.Entity(**entity.model_dump())
    #ic(db_entity)
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

def update_entity(db: Session, entity_id: int, entity: schema_entity.EntityUpdate):
    db_entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if db_entity:
        update_data = entity.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_entity, key, value)
        db.commit()
        db.refresh(db_entity)
    return db_entity

def delete_entity(db: Session, entity_id: int):
    db_entity = db.query(models.Entity).filter(models.Entity.id == entity_id).first()
    if db_entity:
        db.delete(db_entity)
        db.commit()
    return db_entity