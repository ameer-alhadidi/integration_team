from typing import List
from fastapi import   HTTPException, Depends, APIRouter, Response,status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func
from icecream import ic

from ..schemas import contact as  schema_contact

from ..database import get_db
from ..crud import  contact as crud_contact


router = APIRouter(
    prefix="/contacts",
    tags=['Contacts']
) 

# class ErrorResponseModel(schema_contact.ResponseModel):
#     reason: str

 
# @router.post("/", status_code=status.HTTP_201_CREATED, summary="Create a contact",response_model=schema_contact.ContactOut,responses={
#     status.HTTP_422_UNPROCESSABLE_ENTITY: {
#         "model": ErrorResponseModel,
#         "description": "Validation Error"
#     }
# } )
@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create a contact",response_model=schema_contact.ContactOut)
def create_contact_new(contact: schema_contact.ContactCreate,  db: Session = Depends(get_db)):
    """
    ## Create a contact with all the information:

        Entity contact information.                
     
    +   **name**: required name of the contact
    +   **email**: required email address
    +   **mobileNumber**: required mobile number
    +   **officeNumber**: required office number

    
    """
    try:
        #ic(contact.__dict__)

        data= crud_contact.create_contact(db=db, contact=contact)
         
        #contact_dict = {key: value for key, value in contact.__dict__.items() if not key.startswith('_')}
        # contact_data = schema_contact.ContactBase.model_validate(data)

        # status = schema_contact.StatusModel(
        #     code="E0000",
        #     description_en="Success",
        #     description_ar="نجاح"
        # )
        return data #schema_contact.ResponseModel(data=contact_data.__dict__, status=status)
    except ValidationError as e:
        # Handle validation errors
        # status.code = "E0001"
        
        # # Customize the validation error message
        # error_messages = []
        # for error in e.errors():
        #     field = error["loc"][-1]
        #     message = error["msg"]
        #     error_messages.append(f"{field}: {message}")
        
        # status.description_en = "Validation Error - " + ", ".join(error_messages)
        # status.description_ar = "خطأ في التحقق من الصحة"
        
        return {"errors": e.errors()} #schema_contact.ResponseModel(data={"errors": e.errors()}, status=status)
         

# @router.post("a/", response_model=schema_contact.ContactBase)
# def create_contact(contact: schema_contact.ContactBase, db: Session = Depends(get_db)):
#     return crud_contact.create_contact(db=db, contact=contact)

 

@router.get("/count", summary="Count Contacts")
def read_contacts( db: Session = Depends(get_db)):

        data= crud_contact.count_contacts(db)
        
        return {"data":data} #schema_contact.ResponseModel(data=contact_data.__dict__, status=status)
  
    
@router.get("/", summary="List Contacts",response_model=schema_contact.ContactListOut)
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        data= crud_contact.get_contacts(db, skip=skip, limit=limit)
        
        contact_data = schema_contact.ContactListOut(contacts=data)
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
        return e.errors() #schema_contact.ResponseModel(data=e.errors(), status=status)
    

@router.get("/{contact_id}", response_model=schema_contact.ContactBase)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud_contact.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=schema_contact.ContactBase)
def update_contact(contact_id: int, contact: schema_contact.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud_contact.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud_contact.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}