from pydantic import BaseModel

from pydantic_models.review_schema import ReviewModel

""" Pydantic model for Favorite data """
class FavoriteModel(BaseModel):
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[ReviewModel]