from typing import List
from fastapi import   HTTPException, Depends, APIRouter, Response,status
from sqlalchemy.orm import Session
from sqlalchemy import func
from icecream import ic

from ..schemas import port as  schema_port

from ..database import get_db
from ..crud import  port as crud_port

router = APIRouter(
    prefix="/ports",
    tags=['Ports']
)

@router.get("/", response_model=schema_port.PortListOut)
def read_ports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ports = crud_port.get_ports(db, skip=skip, limit=limit)
    total_count = crud_port.count_ports(db)
    return {"ports": ports, "total_count": total_count}

@router.get("/{port_id}", response_model=schema_port.PortOut)
def read_port(port_id: int, db: Session = Depends(get_db)):
    db_port = crud_port.get_port(db, port_id=port_id)
    if db_port is None:
        raise HTTPException(status_code=404, detail="Port not found")
    return db_port

@router.post("/", response_model=schema_port.PortOut)
def create_port(port: schema_port.PortCreate, db: Session = Depends(get_db)):
    return crud_port.create_port(db=db, port=port)

@router.put("/{port_id}", response_model=schema_port.PortOut)
def update_port(port_id: int, port: schema_port.PortUpdate, db: Session = Depends(get_db)):
    db_port = crud_port.get_port(db, port_id=port_id)
    if db_port is None:
        raise HTTPException(status_code=404, detail="Port not found")
    return crud_port.update_port(db=db, port_id=port_id, port=port)

@router.delete("/{port_id}")
def delete_port(port_id: int, db: Session = Depends(get_db)):
    db_port = crud_port.get_port(db, port_id=port_id)
    if db_port is None:
        raise HTTPException(status_code=404, detail="Port not found")
    db.delete(db_port)
    db.commit()
    return {"message": "Port deleted successfully"}