from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
import os
from dotenv import load_dotenv

from mock_data.mock_restaurants_db import DB
from restaurant_modules.restaurant import Restaurant

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
    
#! ----------- User CRUD REST APIs and Authentication ------------###
    
#! ------------- Restaurant CRUD REST APIs ---------------------- ###

""" Creates a new restaurant """
@app.post("/api/new_restaurant", response_model=Restaurant)
def create_restaurant( restaurant: Restaurant):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = """
            INSERT INTO restaurant_schema.restaurants (category, name, address, contact_number, rating)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (restaurant.category, restaurant.name, restaurant.address, restaurant.contact_number, restaurant.rating))
        conn.commit()
        return JSONResponse(content={"message": "Restaurant created successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Creates a new restaurant in Mock Data """
@app.post("/api/mock_restaurant", response_model=Restaurant)
def create_mock_restaurant(restaurant: Restaurant):
    DB.append(restaurant.model_dump())
    return restaurant
        
""" Returns the entire list of restaurants """
@app.get("/api/restaurants", response_model=list[Restaurant])
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
                r.category,
                r.name AS name,
                r.address,
                r.contact_number,
                r.rating AS rating,
                r.is_favorite,
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
                 r.id, r.category, r.name, r.address, r.contact_number, r.rating, r.is_favorite
            ORDER BY r.id ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        [desc[0] for desc in cursor.description]
        
        restaurant_list = []
        for row in rows:
            restaurant_data: Restaurant = {
                "id": row[0],
                "category": row[1],
                "name": row[2],
                "address": row[3],
                "contact_number": row[4],
                "rating": float(row[5]), # Convert Decimal to float for JSON serialization
                "is_favorite": row[6],
                "reviews": row[7] if row[7] else [] # Use the aggregated JSON for reviews
            }

            restaurant_list.append(restaurant_data)

        return restaurant_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Returns the restaurant with the matching name """
@app.get("/api/restaurants_by_name/{restaurant_name}", response_model=list[Restaurant])
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
                r.category,
                r.name AS name,
                r.address,
                r.contact_number,
                r.rating AS rating,
                r.is_favorite,
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
                r.id, r.category, r.name, r.address, r.contact_number, r.rating, r.is_favorite
            ORDER BY r.name ASC;
        """
        # Convert restaurant_name to lowercase for case-insensitive search
        restaurant_name = restaurant_name.lower()
        # Replace spaces with % for SQL wildcard search
        restaurant_name = restaurant_name.replace(" ", "%")
        cursor.execute(query, {"restaurant_name": f'%{restaurant_name}%'})
        rows = cursor.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        [desc[0] for desc in cursor.description]
        
        restaurant_list = []
        for row in rows:
            restaurant_data: Restaurant = {
                "id": row[0],
                "category": row[1],
                "name": row[2],
                "address": row[3],
                "contact_number": row[4],
                "rating": float(row[5]), # Convert Decimal to float for JSON serialization
                "is_favorite": bool(row[6]), # Convert boolean to bool for JSON serialization
                "reviews": row[7] if row[7] else [] # Use the aggregated JSON for reviews
            }

            restaurant_list.append(restaurant_data)

        if restaurant_list == []:
            raise HTTPException(status_code=500, detail="Restaurant not found")

        return restaurant_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Returns the restaurant with the specified ID """
@app.get("/api/restaurant/{id}", response_model=Restaurant)
async def get_restaurant(id: int):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id AS id,
                r.category,
                r.name AS name,
                r.address,
                r.contact_number,
                r.rating AS rating,
                r.is_favorite,
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
        [desc[0] for desc in cursor.description]
        
        restaurant_data: Restaurant = {
            "id": rows[0][0],
            "category": rows[0][1],
            "name": rows[0][2],
            "address": rows[0][3],
            "contact_number": rows[0][4],
            "rating": rows[0][5], # Convert Decimal to float for JSON serialization
            "is_favorite": bool(rows[0][6]), # Convert boolean to bool for JSON serialization
            "reviews": []
        }
        

        for row in rows:
            if row[5]: # Check if there is a review for this restaurant
                review = {
                    "username": row[7],
                    "review": row[8],
                    "rating": float(row[9]) # Convert Decimal to float for JSON serialization
                }
                restaurant_data["reviews"].append(review)

        return restaurant_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Returns the recommended list of restaurants """
@app.get("/api/restaurants/recommended", response_model=list[Restaurant])
async def get_recommended_restaurants():
    restaurant_list = [
        {
            "id": restaurant["id"],
            "category": restaurant["category"],
            "name": restaurant["name"],
            "address": restaurant["address"],
            "contact_number": restaurant["contact_number"],
            "rating": restaurant["rating"],
            "is_favorite": restaurant["is_favorite"],
            "reviews": restaurant["reviews"]
        }
        for restaurant in DB
    ]
    return restaurant_list

""" Returns the restaurant with the specified ID """
@app.get("/api/recommended_restaurant/{id}")
def get_restaurant(id: int):  # noqa: F811
    for restaurant in DB:
        if restaurant["id"] == id:
            return restaurant

""" Updates the restaurant with the specified ID in mock database """
# @app.put("/api/mock_update_restaurant/{id}", response_model=Restaurant)
# async def update_restaurant_mock(id: int, restaurant: Restaurant):
#     for restaurant in DB:
#         if restaurant["id"] == id:
#             restaurant.update(restaurant)
#     return DB

""" Updates the restaurant with the specified ID """
@app.patch("/api/update_restaurant/{id}", response_model=Restaurant)
async def update_restaurant(id: int, restaurant: Restaurant):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        existing_restaurant_query = "SELECT * FROM restaurant_schema.restaurants WHERE id = %s"
        cursor.execute(existing_restaurant_query, [id,])
        existing_restaurant = cursor.fetchone()
        if not existing_restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Convert the Row object to a dictionary
        column_names = [desc[0] for desc in cursor.description]
        existing_restaurant = dict(zip(column_names, existing_restaurant))

        # Update the existing restaurant with the new data from the request
        update_data = restaurant.model_dump(exclude_unset=True)
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE restaurant_schema.restaurants SET {set_clause} WHERE id = %s"
        values = list(update_data.values()) + [id]
        cursor.execute(query, values)
        conn.commit()
        updated_restaurant = {**existing_restaurant, **update_data}
        print("Updated restaurant:", updated_restaurant)
        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

""" Deletes the restaurant with the specified ID """
  # TODO: Consider and define business logic for deleting a restaurant in relation to reviews.
@app.delete("/api/delete_restaurant/{id}")
async def delete_restaurant(id: int):
    conn = connect_to_database()
    if not conn:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    try:
        print("Connected to the database!")
        cursor = conn.cursor()
        query = "DELETE FROM restaurant_schema.restaurants WHERE id = %s;"
        cursor.execute(query, (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=500, detail=f"Restaurant with specified ID {id} not found")
        conn.commit()
        return {"message": "Restaurant deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
