from pydantic import BaseModel

from pydantic_models.review_schema import ReviewModel

""" Pydantic model for Restaurant Create and Update data """
class RestaurantCreate(BaseModel):
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[ReviewModel] = []

    model_config = {}
    model_config['from_attributes'] = True

class RestaurantUpdate(BaseModel):
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[ReviewModel] = []

    model_config = {}
    model_config['from_attributes'] = True
