from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Restaurant(BaseModel):
    name: str
    address: str
    contact_number: str
    rating: float
    reviews: List

# Mock database in json format
DB: list[Restaurant] = [{
        "name": "The Gourmet Kitchen",
        "address": "123 Maple Street, Springfield, IL 62704",
        "contact_number": "(217) 555-1234",
        "rating": 4.5,
        "reviews": [
            {
                "username": "foodie123",
                "review": "Amazing food and great ambiance!",
                "rating": 5
            },
            {
                "username": "janedoe",
                "review": "Good selection, but a bit pricey.",
                "rating": 4
            }
        ]
    },
{
        "name": "Pizza Paradise",
        "address": "456 Elm Avenue, Springfield, IL 62705",
        "contact_number": "(217) 555-5678",
        "rating": 4.7,
        "reviews": [
            {
                "username": "pizzalover",
                "review": "Best pizza in town! Highly recommend the Margherita.",
                "rating": 5
            },
            {
                "username": "johnsmith",
                "review": "Great pizza but the service was slow.",
                "rating": 4
            }
        ]
    },
{
        "name": "Sushi World",
        "address": "789 Oak Street, Springfield, IL 62706",
        "contact_number": "(217) 555-9012",
        "rating": 4.3,
        "reviews": [
            {
                "username": "sushifan",
                "review": "Fresh sushi and friendly staff.",
                "rating": 5
            },
            {
                "username": "michelles",
                "review": "Good sushi but portions are small.",
                "rating": 4
            }
        ]
    },
{
        "name": "Curry House",
        "address": "101 Pine Lane, Springfield, IL 62707",
        "contact_number": "(217) 555-3456",
        "rating": 4.6,
        "reviews": [
            {
                "username": "spicylover",
                "review": "Authentic Indian food with the perfect amount of spice.",
                "rating": 5
            },
            {
                "username": "lukewarm",
                "review": "Food was good but service could be better.",
                "rating": 4
            }
        ]
    },
{
        "name": "Burger Barn",
        "address": "202 Birch Road, Springfield, IL 62708",
        "contact_number": "(217) 555-7890",
        "rating": 4.2,
        "reviews": [
            {
                "username": "burgerking",
                "review": "Juicy burgers and crispy fries!",
                "rating": 5
            },
            {
                "username": "anonymouse",
                "review": "Burgers were decent, but the place was crowded.",
                "rating": 3
            }
        ]
    }]


@app.get("/api/restaurants")
def read_root():
    return DB


# @app.get("/api/people")
# def read_people():
#     return DB