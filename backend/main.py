from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT'),
}

def connect_to_database():
    try:
        print("Connecting to the PostgreSQL database...")
        # Establish connection
        conn = psycopg2.connect(**db_config)
        return conn

    except Exception as e:
        print("Error connecting to PostgreSQL database: ", e)
        return None

class Review(BaseModel):
    username: str
    review: str
    rating: float

class Restaurant(BaseModel):
    id: int
    name: str
    address: str
    contact_number: str
    rating: float
    isFavorite: bool = False
    reviews: List[Review] = []

# Mock database in json format
DB: list[Restaurant] = [{
        "id": 1,
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
        "id": 2,
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
        "id": 3,
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
        "id": 4,
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
        "id": 5,
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

""" Returns the entire list of restaurants """
@app.get("/api/restaurants")
async def get_restaurants():
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id AS id,
                r.name AS name,
                r.address,
                r.contact_number,
                r.rating AS rating,
                COALESCE(
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'username', rv.username,
                            'review', rv.review,
                            'rating', rv.rating
                        )
                    ) FILTER (WHERE rv.username IS NOT NULL), '[]'
                ) AS reviews
            FROM 
                restaurant_schema.restaurants r
            LEFT JOIN 
                restaurant_schema.reviews rv ON r.id = rv.restaurant_id
            GROUP BY
                 r.id, r.name, r.address, r.contact_number, r.rating
            ORDER BY r.id ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        colnames = [desc[0] for desc in cursor.description]
        
        restaurant_list = []
        for row in rows:
            restaurant_data = {
                "id": row[0],
                "name": row[1],
                "address": row[2],
                "contact_number": row[3],
                "rating": float(row[4]), # Convert Decimal to float for JSON serialization
                "reviews": row[5] if row[5] else [] # Use the aggregated JSON for reviews
            }

            restaurant_list.append(restaurant_data)

        return restaurant_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Returns the restaurant with the matching name """
@app.get("/api/restaurants_by_name/{restaurant_name}")
async def get_restaurants_by_name(restaurant_name: str):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id AS id,
                r.name AS name,
                r.address,
                r.contact_number,
                r.rating AS rating,
                COALESCE(
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'username', rv.username,
                            'review', rv.review,
                            'rating', rv.rating
                        )
                    ) FILTER (WHERE rv.username IS NOT NULL), '[]'
                ) AS reviews
            FROM 
                restaurant_schema.restaurants r
            LEFT JOIN 
                restaurant_schema.reviews rv ON r.id = rv.restaurant_id
            WHERE
                LOWER(r.name) LIKE %(restaurant_name)s
            GROUP BY
                r.id, r.name, r.address, r.contact_number, r.rating
            ORDER BY r.name DESC;
        """
        # Convert restaurant_name to lowercase for case-insensitive search
        restaurant_name = restaurant_name.lower()
        # Replace spaces with % for SQL wildcard search
        restaurant_name = restaurant_name.replace(" ", "%")
        cursor.execute(query, {"restaurant_name": f'%{restaurant_name}%'})
        rows = cursor.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        colnames = [desc[0] for desc in cursor.description]
        
        restaurant_list = []
        for row in rows:
            restaurant_data = {
                "id": row[0],
                "name": row[1],
                "address": row[2],
                "contact_number": row[3],
                "rating": float(row[4]), # Convert Decimal to float for JSON serialization
                "reviews": row[5] if row[5] else [] # Use the aggregated JSON for reviews
            }

            restaurant_list.append(restaurant_data)

        return restaurant_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Creates a new restaurant """
@app.post("/api/restaurant")
def create_restaurant(restaurant: Restaurant):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = """
            INSERT INTO restaurant_schema.restaurants (name, address, contact_number, rating)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query, (restaurant.name, restaurant.address, restaurant.contact_number, restaurant.rating))
        conn.commit()
        return JSONResponse(content={"message": "Restaurant created successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Returns the restaurant with the specified ID """
@app.get("/api/restaurant/{id}", response_model=Restaurant)
def get_restaurant(id: int):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id AS id,
                r.name AS name,
                r.address,
                r.contact_number,
                r.rating AS rating,
                rv.username,
                rv.review,
                rv.rating AS rating
            FROM 
                restaurant_schema.restaurants r
            LEFT JOIN 
                restaurant_schema.reviews rv ON r.id = rv.restaurant_id
            WHERE r.id = %s;
        """
        cursor.execute(query, (id,))
        rows = cursor.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        colnames = [desc[0] for desc in cursor.description]
        
        restaurant_data = {
            "id": rows[0][0],
            "name": rows[0][1],
            "address": rows[0][2],
            "contact_number": rows[0][3],
            "rating": float(rows[0][4]), # Convert Decimal to float for JSON serialization
            "reviews": []
        }
        

        for row in rows:
            if row[5]: # Check if there is a review for this restaurant
                review = {
                    "username": row[5],
                    "review": row[6],
                    "rating": float(row[7]) # Convert Decimal to float for JSON serialization
                }
                restaurant_data["reviews"].append(review)

        return restaurant_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Returns the recommended list of restaurants """
@app.get("/api/restaurants/recommended")
def get_recommended_restaurants():
    restaurant_list = [
        {
            "id": restaurant["id"],
            "name": restaurant["name"],
            "address": restaurant["address"],
            "contact_number": restaurant["contact_number"],
            "rating": restaurant["rating"],
            "reviews": restaurant["reviews"]
        }
        for restaurant in DB
    ]
    return restaurant_list

""" Returns the restaurant with the specified ID """
@app.get("/api/recommended_restaurant/{id}")
def get_restaurant(id: int):
    for restaurant in DB:
        if restaurant["id"] == id:
            return restaurant

""" Updates the restaurant with the specified ID """
@app.put("/api/update_restaurant/{id}")
def update_restaurant(id: int, restaurant: Restaurant):
    for restaurant in DB:
        if restaurant["id"] == id:
            restaurant.update(restaurant)
    return DB