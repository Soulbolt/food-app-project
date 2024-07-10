from pydantic import BaseModel


""" Pydantic model for Review data """
class ReviewModel(BaseModel):
    id: int
    username: str
    review: str
    rating: float
    restaurant_id: int

    model_config = {}
    model_config['from_attributes'] = True