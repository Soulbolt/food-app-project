from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Restaurant(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int

DB: List[Restaurant] = [
    Restaurant(id=1, first_name="John", last_name="Duh", age=20),
    Restaurant(id=2, first_name="Jane", last_name="Flex", age=21),
    Restaurant(id=3, first_name="Joe", last_name="Muff", age=22),
    Restaurant(id=4, first_name="Jill", last_name="Dill", age=23),
]

@app.get("/api")
def read_root():
    return DB


# @app.get("/api/people")
# def read_people():
#     return DB