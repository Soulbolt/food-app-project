from pydantic import BaseModel
from roles import Role

class TokenData(BaseModel):
    username: str
    roles: list[Role]