from sqlalchemy import Column, Integer, String, Float, Boolean
from database_models.base import Base

""" SQLAlchemy model for Favorites """
class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, index=True)
    category= Column(String)
    name= Column(String)
    address= Column(String)
    contact_number= Column(String)
    rating= Column(Float)
    is_favorite= Column(Boolean)
    reviews= Column(String)