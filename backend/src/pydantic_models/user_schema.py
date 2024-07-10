from pydantic import BaseModel

from pydantic_models.favorite_schema import FavoriteModel

""" Pydantic model for UserCreate and UseCredentials data"""
class UserCreateModel(BaseModel):
    email: str
    password: str
    username: str
    name: str
    favorites: list[FavoriteModel]

class UserCredentials(BaseModel):
    username: str
    password: str