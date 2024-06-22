from pydantic import BaseModel
from typing import List

""" Pydantic models for Restaurant and Review data """
class Review(BaseModel):
    username: str
    review: str
    rating: float

class Restaurant(BaseModel):
    id: int
    name: str
    address: str
    contact_number: str
    rating: float
    isFavorite: bool = False
    reviews: List[Review] = []