from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database_models.base import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
RCMD_DATABASE_URL = os.getenv("RCMD_DATABASE_URL")
# conditional for apply schema name when postgresql is used
SCHEMA_NAME = "restaurant_schema" if DATABASE_URL and DATABASE_URL.startswith("postgresql") else None

""" SqlAlchemy Resturant Model for Restaurant data """
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
