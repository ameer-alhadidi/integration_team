from sqlalchemy.orm import Session
from icecream import ic
from ..models import models
from ..schemas import port as schema_port

def count_ports(db: Session):
    return db.query(models.Port).count()

def get_port(db: Session, port_id: int):
    return db.query(models.Port).filter(models.Port.id == port_id).first()

def get_ports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Port).offset(skip).limit(limit).all()

def create_port(db: Session, port: schema_port.PortCreate):
    db_port = models.Port(
        number=port.number,
        service_access=port.service_access,
        allowed_access=port.allowed_access,
        entity_id=port.entity_id,
        created_by=port.created_by,
        updated_by=port.updated_by
    )
    db.add(db_port)
    db.commit()
    db.refresh(db_port)
    return db_port

def update_port(db: Session, port_id: int, port: schema_port.PortUpdate):
    db_port = db.query(models.Port).filter(models.Port.id == port_id).first()
    if db_port:
        for var, value in vars(models.Port).items():
            setattr(db_port, var, value) if value else None
        db.add(db_port)
        db.commit()
        db.refresh(db_port)
        return db_port