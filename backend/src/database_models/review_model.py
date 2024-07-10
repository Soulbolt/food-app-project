from sqlalchemy import ForeignKey, Integer, String, Column, Float
from sqlalchemy.orm import relationship
from database_models.restaurant_model import SCHEMA_NAME
from base import Base


""" SQLAlchmey Review Model for Review data"""
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