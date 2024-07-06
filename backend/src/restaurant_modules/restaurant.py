from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
# Base class for ORM models, I want to make sure that the relationship between the Restaurant and Review models is properly defined.
""" SqlAlchemy table models for Restaurant and Review data """
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    review= Column(String)
    rating= Column(Float)
    restaurant_id= Column(Integer, ForeignKey('restaurants.id'))
    # Relationship between the Restaurant and Review models
    restaurant = relationship("Restaurant", back_populates="reviews")

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id= Column(Integer, primary_key=True, index=True)
    category= Column(String)
    name= Column(String)
    address= Column(String)
    contact_number= Column(String)
    rating= Column(Float)
    is_favorite= Column(Boolean)
    # Define the relationship between the Restaurant and Review models
    reviews= relationship("Review", back_populates="restaurant")

""" Pydantic models for Restaurant and Review data """
class ReviewModel(BaseModel):
    # id: int
    username: str
    review: str
    rating: float
    # restaurant_id: int

    model_config = {}
    model_config['from_attributes'] = True

class RestaurantModel(BaseModel):
    id: int
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[ReviewModel] = []

    model_config = {}
    model_config['from_attributes'] = True
