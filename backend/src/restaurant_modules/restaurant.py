from pydantic import BaseModel
from typing import List, Optional

""" Pydantic models for Restaurant and Review data """
class Review(BaseModel):
    username: str
    review: str
    rating: float

class Restaurant(BaseModel):
    id: Optional[int] = None
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool = False
    reviews: List[Review] = []