from pydantic import BaseModel

""" Pydantic model for User data and Favorites """
class User(BaseModel):
    id: int
    email: str
    password: str
    username: str
    name: str
    favorites: []


