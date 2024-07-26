from pydantic import BaseModel
from typing import List


class NoteBase(BaseModel):
    title:str
    content:str
    class Config():
        from_attributes  = True

class Note(NoteBase):
    class Config():
        from_attributes  = True

class User(BaseModel):
    username:str
    email: str
    password:str

class ShowUser(BaseModel):
    username:str
    email: str
    note:List[Note]=[]
    class Config():
        from_attributes  = True

class ShowNote(BaseModel):
    title:str
    content:str
    creator:ShowUser

    class Config():
        from_attributes  = True
    
class Login(BaseModel):
    username:str
    password:str
   
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
