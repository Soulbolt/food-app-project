from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Base class for ORM models, I want to make sure that the relationship between the Restaurant and Review models is properly defined.
""" Pydantic models for Restaurant and Review data """
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