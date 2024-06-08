from typing import List
from fastapi import   HTTPException, Depends, APIRouter, Response,status
from pydantic import TypeAdapter, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func
from icecream import ic

from ..schemas import entity as  schema_entity

from ..database import get_db
from ..crud import  entity as crud_entity


router = APIRouter(
    prefix="/entities",
    tags=['Entities']
) 

@router.post("/", response_model=schema_entity.EntityInDB)
def create_entity(entity: schema_entity.EntityCreate, db: Session = Depends(get_db)):
    return crud_entity.create_entity(db=db, entity=entity)

@router.get("/", summary="List entities without contacts")
def read_entities_no_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data= crud_entity.get_entities_no_contacts(db, skip=skip, limit=limit)
        contact_data = schema_entity.EntitiyOnlyListOut(entities=data)
        return  contact_data #schema_contact.ResponseModel(data=contact_data.__dict__, status=status)
       
    except ValidationError as e:
        return e.errors() #schema_contact.ResponseModel(data=e.errors(), status=status)d
    
@router.get("/contacts", summary="List Entities")#,response_model=schema_entity.EntityBase)
def read_entities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        data= crud_entity.get_entities(db, skip=skip, limit=limit)
        contact_data = schema_entity.EntitiyListOut(entities=data)
        #entity_data = schema_entity.EntityBase.model_validate(entity_dict)
        #ic(m.model_dump())
        # status = schema_contact.StatusModel(
        #     code="E0000",
        #     description_en="Success",
        #     description_ar="نجاح"
        # )
        return  contact_data #schema_contact.ResponseModel(data=contact_data.__dict__, status=status)
       
    except ValidationError as e:
        # status = schema_contact.StatusModel(
        #     code="E0001",
        #     description_en="Validation Error",
        #     description_ar="خطأ"
        # )
        return e.errors() #schema_contact.ResponseModel(data=e.errors(), status=status)d