from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str



    

class VersionBase(BaseModel):
    minor_version: str
    release_date: date
    

class VersionCreate(VersionBase):
    pass

class VersionResponse(VersionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
