import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from icecream import ic


#load config data
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#ic(BASE_DIR)

load_dotenv(dotenv_path=os.path.join(BASE_DIR,"..", ".env"))

#serialize values
class Settings(BaseSettings):
    project_name: str = "Integration Team"
    project_version: str = "0.0.1"
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
#ic(settings)
#ic(settings.database_username)
#settings = Settings().model_dump()
#ic(settings)