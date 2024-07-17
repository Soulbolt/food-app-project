from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime as DateTime

""" Pydantic model for User Model data """
class UserModel(BaseModel):
    id: Optional[int]
    email: EmailStr
    username: str
    name: str
    favorites: list
    token_expired: Optional[DateTime]
    token: Optional[str]

    model_config = {}
    model_config['from_attributes'] = True