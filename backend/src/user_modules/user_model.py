from pydantic import BaseModel

""" Pydantic model for User data """
class User(BaseModel):
    username: str
    name: str

