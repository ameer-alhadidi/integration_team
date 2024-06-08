from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import entity, contact
 
# from . import models
# from .database import engine
#from .routers import contact
# from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact.router)
app.include_router(entity.router)
# app.include_router(auth.router)
# app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to Windows"}