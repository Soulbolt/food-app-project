import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src/restaurant_modules"))
from restaurant import Restaurant, Review 
import sqlite3

# Mock database in json format
# class DB:
#     def __init__(self):
#         self.DB = self.generate_mock_db()

#     f generate_mock_db(self):
DB: list[Restaurant] = []

def get_mock_data():
    return [
        {
            "id": 1,
            "category": "Italian",
            "name": "The Gourmet Kitchen",
            "address": "123 Maple Street, Springfield, IL 62704",
            "contact_number": "(217) 555-1234",
            "rating": 4.5,
            "is_favorite": True,
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
            "id": 2,
            "category": "Italian",
            "name": "Pizza Paradise",
            "address": "456 Elm Avenue, Springfield, IL 62705",
            "contact_number": "(217) 555-5678",
            "rating": 4.7,
            "is_favorite": True,
            "reviews": [
                {
                    "username": "sarahjones",
                    "review": "The best pizza I've ever had. I love it!",
                    "rating": 5
                },
                {
                    "username": "johndoe",
                    "review": "I had the cheese and tomato pizza.",
                    "rating": 3
                }
            ]
        },
        {
            "id": 3,
            "category": "Indian",
            "name": "Thai Curry House",
            "address": "789 Oak Road, Springfield, IL 62706",
            "contact_number": "(217) 555-9012",
            "rating": 4.3,
            "is_favorite": True,
            "reviews": [
                {
                    "username": "thaichef",
                    "review": "The best curry I've ever had. I love it!",
                    "rating": 5
                },
                {
                    "username": "johndoe",
                    "review": "I had the chicken and rice curry.",
                    "rating": 3
                }
            ]
        },
        {
        "id": 4,
        "category": "Thai",
        "name": "Curry House",
        "address": "101 Pine Lane, Springfield, IL 62707",
        "contact_number": "(217) 555-3456",
        "rating": 4.6,
        "is_favorite": True,
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
        "id": 5,
        "category": "American",
        "name": "Burger Barn",
        "address": "202 Birch Road, Springfield, IL 62708",
        "contact_number": "(217) 555-7890",
        "rating": 4.2,
        "is_favorite": True,
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
    }
]
def create_restaurants_table():
    conn = sqlite3.connect('rcmd_restaurants.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants
                 (id INTEGER PRIMARY KEY,
                 category TEXT,
                 name TEXT,
                 address TEXT,
                 contact_number TEXT,
                 rating REAL,
                 is_favorite INTEGER)''')
    conn.commit()
    conn.close()

def create_reviews_table():
    conn = sqlite3.connect('rcmd_restaurants.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews
                 (id INTEGER PRIMARY KEY,
                 username TEXT,
                 review TEXT,
                 rating INTEGER,
                 restaurant_id INTEGER,
                 FOREIGN KEY (restaurant_id) REFERENCES restaurants (id))''')
    conn.commit()
    conn.close()

def populate_db():
    conn = sqlite3.connect('rcmd_restaurants.db')
    c = conn.cursor()
    for restaurant in get_mock_data():
        reviews = restaurant.pop("reviews")
        c.execute('''INSERT INTO restaurants (category, name, address, contact_number, rating, is_favorite)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (restaurant["category"], restaurant["name"], restaurant["address"], restaurant["contact_number"],
                   restaurant["rating"], restaurant["is_favorite"]))
        restaurant_id = c.lastrowid
        for review in reviews:
            c.execute('''INSERT INTO reviews (username, review, rating, restaurant_id)
                         VALUES (?, ?, ?, ?)''',
                      (review["username"], review["review"], review["rating"], restaurant_id))
    conn.commit()
    conn.close()

create_restaurants_table()
create_reviews_table()
populate_db()
