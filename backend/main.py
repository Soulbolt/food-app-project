from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str
    age: int

DB: List[Person] = [
    Person(id=1, name="John", age=20),
    Person(id=2, name="Jane", age=21),
    Person(id=3, name="Joe", age=22),
    Person(id=4, name="Jill", age=23),
]

@app.get("/api")
def read_root():
    return DB


# @app.get("/api/people")
# def read_people():
#     return DB