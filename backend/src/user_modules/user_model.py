from pydantic import BaseModel
from restaurant import Restaurant, Review

""" Pydantic model for User data and Favorites """
class Favorite(BaseModel):
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[Review] = []
    
class User(BaseModel):
    id: int
    email: str
    password: str
    username: str
    name: str
    favorites: list[Favorite] = []

