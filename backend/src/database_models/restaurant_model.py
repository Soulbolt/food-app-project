from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
RCMD_DATABASE_URL = os.getenv("RCMD_DATABASE_URL")

Base = declarative_base()
SCHEMA_NAME = "restaurant_schema" if DATABASE_URL and DATABASE_URL.startswith("postgresql") else None

# Base class for ORM models, I want to make sure that the relationship between the Restaurant and Review models is properly defined.
""" SqlAlchemy table models for Restaurant and Review data """
class Restaurant(Base):
    __tablename__ = 'restaurants'
    # Conditionally set __table_args__
    __table_args__ = {'schema': SCHEMA_NAME} if SCHEMA_NAME else {}
    id= Column(Integer, primary_key=True, index=True)
    category= Column(String)
    name= Column(String)
    address= Column(String)
    contact_number= Column(String)
    rating= Column(Float)
    is_favorite= Column(Boolean)
    # Define the relationship between the Restaurant and Review models
    reviews= relationship("Review", back_populates="restaurant")
    
class Review(Base):
    __tablename__ = 'reviews'
    # Conditionally set __table_args__
    __table_args__ = {'schema': SCHEMA_NAME} if SCHEMA_NAME else {}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    review= Column(String)
    rating= Column(Float)
    restaurant_id= Column(Integer, ForeignKey(f"{SCHEMA_NAME + '.' if SCHEMA_NAME else ''}restaurants.id"))
    # Relationship between the Restaurant and Review models
    restaurant = relationship("Restaurant", back_populates="reviews")

""" Pydantic models for Restaurant and Review data """
class ReviewModel(BaseModel):
    id: int
    username: str
    review: str
    rating: float
    restaurant_id: int

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

class Settings(BaseSettings):
    if DATABASE_URL:
        primary_database_url: str = DATABASE_URL
    else:
        raise ValueError("DATABASE_URL must be set in .env file")

    if RCMD_DATABASE_URL:
        secondary_database_url: str = RCMD_DATABASE_URL
    else:
        raise ValueError("RCMD_DATABASE_URL must be set in .env file")
    
    class Config:
        env_file = ".env"
