from pydantic import BaseModel

from database_models.review_model import Review

""" Pydantic model for Favorite data """
class FavoriteModel(BaseModel):
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[Review]