from pydantic import BaseModel
from restaurant import Restaurant

""" Pydantic model for User data and Favorites """
class User(BaseModel):
    id: int
    email: str
    password: str
    username: str
    name: str
    favorites: list[Restaurant] = []


