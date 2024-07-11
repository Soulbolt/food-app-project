from pydantic import BaseModel, EmailStr

""" Pydantic model for UserCreate and UseCredentials data"""
class UserCreateModel(BaseModel):
    username: str
    email: EmailStr
    hash_password: str
    name: str

class UserCredentials(BaseModel):
    username: str
    password: str