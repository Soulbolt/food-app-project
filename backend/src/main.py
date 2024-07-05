from typing import Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
import psycopg2
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

from mock_data.mock_restaurants_db import DB
from restaurant_modules.restaurant import Restaurant, Review
from user_modules.user_model import UserCredentials, User, Base
from mock_data.mock_users_db import USER_DB

# Load environment variables
load_dotenv()

# Passlib context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = os.getenv("DATABASE_URL")

# Create a database engine
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    raise ValueError("DATABASE_URL is not set.")

# Create a SessionalLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a FastAPI instance
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

def get_database_connection_string():
    # Check if we are in a testing environment
    if os.getenv("ENV") == 'test':
        return os.getenv('TEST_DATABASE_URL')
    else:
        return os.getenv('DATABASE_URL')

def connect_to_database():
    database_url = get_database_connection_string()
    try:
        if database_url and database_url.startswith("postgres://"):
            print("Connecting to the PostgreSQL database...")
            # Establish connection
            conn = psycopg2.connect(
                host=db_config['host'],
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password'],
                port=db_config['port']
            )
            return conn
        elif database_url and database_url.startswith("sqlite://"):
            # Establish connection
            print("Connecting to the SQLite database...")
            # Extract the file path from the url
            db_file_path = database_url.replace("sqlite:///", "")
            conn = sqlite3.connect(db_file_path, check_same_thread=False)
            return conn

    except Exception as e:
        print("Error connecting to database: ", e)
        return None
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
    
#* ----------- User CRUD REST APIs and Authentication ------------###
""" create new User """
# TODO: Create REST API to create new user.
async def create_user(db: Session, user_data):
    db_user = User(username=user_data.username, email=user_data.email, hashed_password=user_data.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

""" Authenticate Existing User """
async def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/api/authenticate/")
async def authenticate(db, credentials: UserCredentials):
    user = authenticate_user(db, credentials.username, credentials.password)
    if user:
        return {"message": "Authentication successful!", "user": user}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
""" Update Existing User """
# TODO: Create REST API to edit an existing users properties/settings.

#* ------------- Restaurant CRUD REST APIs ---------------------- ###

""" Creates a new restaurant """
@app.post("/api/new_restaurant", response_model=Restaurant)
async def create_restaurant(db: Session, restaurant_data):
    # conn = connect_to_database()
    db_restaurant = Restaurant(**restaurant_data)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant
    # if not conn:
    #     raise HTTPException(status_code=500, detail="Could not connect to the database")
    # try:
    #     print("Connected to the database!")
    #     cursor = conn.cursor()
    #     query = """
    #         INSERT INTO restaurant_schema.restaurants (category, name, address, contact_number, rating)
    #         VALUES (%s, %s, %s, %s, %s);
    #     """
    #     cursor.execute(query, (restaurant.category, restaurant.name, restaurant.address, restaurant.contact_number, restaurant.rating))
    #     conn.commit()
    #     return JSONResponse(content={"message": "Restaurant created successfully!"})
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     cursor.close()
    #     conn.close()

""" Creates a new restaurant in Mock Data """
@app.post("/api/mock_restaurant", response_model=Restaurant)
async def create_mock_restaurant(restaurant: Restaurant):
    DB.append(restaurant)
    return restaurant
        
""" Returns the entire list of restaurants """
@app.get("/api/restaurants", response_model=list[Restaurant])
async def get_restaurants(db: Session = Depends(get_database_connection_string), skip: int = 0, limit: int = 100):
    return db.query(Restaurant).offset(skip).limit(limit).all()
    # conn = connect_to_database()
    # if not conn:
    #     raise HTTPException(status_code=500, detail="Could not connect to the database")
    
    # try:
    #     print("Connected to the database!")
    #     cursor = conn.cursor()
    #     query = """
    #         SELECT 
    #             r.id AS id,
    #             r.category,
    #             r.name AS name,
    #             r.address,
    #             r.contact_number,
    #             r.rating AS rating,
    #             r.is_favorite,
    #             COALESCE(
    #                 JSON_AGG(
    #                     JSON_BUILD_OBJECT(
    #                         'username', rv.username,
    #                         'review', rv.review,
    #                         'rating', rv.rating
    #                     )
    #                 ) FILTER (WHERE rv.username IS NOT NULL), '[]'
    #             ) AS reviews
    #         FROM 
    #             restaurant_schema.restaurants r
    #         LEFT JOIN 
    #             restaurant_schema.reviews rv ON r.id = rv.restaurant_id
    #         GROUP BY
    #              r.id, r.category, r.name, r.address, r.contact_number, r.rating, r.is_favorite
    #         ORDER BY r.id ASC;
    #     """
    #     cursor.execute(query)
    #     rows = cursor.fetchall()
    #     if rows is None:
    #         raise HTTPException(status_code=404, detail="Restaurant not found")
        
    #     if cursor.description is not None:
    #         [desc[0] for desc in cursor.description]
        
    #     restaurant_list = []
    #     for row in rows:
    #         restaurant_data: Restaurant = Restaurant(
    #             id=row[0],
    #             category=row[1],
    #             name=row[2],
    #             address=row[3],
    #             contact_number=row[4],
    #             rating=float(row[5]), # Convert Decimal to float for JSON serialization
    #             is_favorite=row[6],
    #             reviews=row[7] if row[7] else [] # Use the aggregated JSON for reviews
    #         )

    #         restaurant_list.append(restaurant_data)

    #     return restaurant_list
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     cursor.close()
    #     conn.close()

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
        
        if cursor.description is not None:
            [desc[0] for desc in cursor.description]
        
        restaurant_list = []
        for row in rows:
            restaurant_data = Restaurant(
                id= row[0],
                category= row[1],
                name= row[2],
                address= row[3],
                contact_number= row[4],
                rating= float(row[5]), # Convert Decimal to float for JSON serialization
                is_favorite= bool(row[6]), # Convert boolean to bool for JSON serialization
                reviews= row[7] if row[7] else [] # Use the aggregated JSON for reviews
            )

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
async def get_restaurant_by_id(db: Session, id: int):
    return db.query(Restaurant).filter(Restaurant.id == id).first()
    # conn = connect_to_database()
    # if not conn:
    #     raise HTTPException(status_code=500, detail="Could not connect to the database")
    # try:
    #     print("Connected to the database!")
    #     cursor = conn.cursor()
    #     query = """
    #         SELECT 
    #             r.id AS id,
    #             r.category,
    #             r.name AS name,
    #             r.address,
    #             r.contact_number,
    #             r.rating AS rating,
    #             r.is_favorite,
    #             rv.username,
    #             rv.review,
    #             rv.rating AS rating
    #         FROM 
    #             restaurant_schema.restaurants r
    #         LEFT JOIN 
    #             restaurant_schema.reviews rv ON r.id = rv.restaurant_id
    #         WHERE r.id = %s;
    #     """
    #     cursor.execute(query, (id,))
    #     rows = cursor.fetchall()
    #     if rows is None:
    #         raise HTTPException(status_code=404, detail="Restaurant not found")
        
    #     if cursor.description is not None:
    #         [desc[0] for desc in cursor.description]
        
    #     restaurant_data = Restaurant(
    #         id=rows[0][0],
    #         category=rows[0][1],
    #         name=rows[0][2],
    #         address=rows[0][3],
    #         contact_number=rows[0][4],
    #         rating=float(rows[0][5]), # Convert Decimal to float for JSON serialization
    #         is_favorite=bool(rows[0][6]), # Convert boolean to bool for JSON serialization
    #         reviews=[]
    #     )
        
    #     for row in rows:
    #         if row[5]: # Check if there is a review for this restaurant
    #             review = Review(
    #                 username=row[7],
    #                 review=row[8],
    #                 rating=float(row[9]) # Convert Decimal to float for JSON serialization
    #             )
    #             restaurant_data.reviews.append(review)
        
    #     return restaurant_data
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     cursor.close()
    #     conn.close()

""" Returns the recommended list of restaurants """
@app.get("/api/restaurants/recommended", response_model=list[dict[str, Any]])
async def get_recommended_restaurants():
    restaurant_list = [
        {
            "id": restaurant.id,
            "category": restaurant.category,
            "name": restaurant.name,
            "address": restaurant.address,
            "contact_number": restaurant.contact_number,
            "rating": restaurant.rating,
            "is_favorite": restaurant.is_favorite,
            "reviews": restaurant.reviews
        }
        for restaurant in DB
    ]
    return restaurant_list

""" Returns the restaurant with the specified ID """
@app.get("/api/recommended_restaurant/{id}")
def get_restaurant(id: int):  # noqa: F811
    for restaurant in DB:
        if restaurant.id == id:
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
        if cursor.description is not None:
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
