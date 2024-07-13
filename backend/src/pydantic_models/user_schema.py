from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime as DateTime

""" Pydantic model for User Model data """
class User(BaseModel):
    id: Optional[int]
    email: str
    username: str
    name: str
    favorites: list
    password_reset_token_expires: Optional[DateTime]
    password_reset_token: Optional[str]

    model_config = {}
    model_config['from_attributes'] = True