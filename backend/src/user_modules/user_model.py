from pydantic import BaseModel
from restaurant_modules.restaurant import Restaurant, Review

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

class UserCredentials(BaseModel):
    email: str
    password: str

class UserInDB(User):
    hashed_password: str
    class Config:
        orm_mode = True

class UserInResponse(BaseModel):
    id: int
    email: str
    username: str
    name: str
    favorites: list[Favorite]
    class Config:
        orm_mode = True

class UserInResponseWithToken(UserInResponse):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: str
    password: str
    username: str
    name: str
    class Config:
        orm_mode = True


