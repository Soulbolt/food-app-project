from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from restaurant_modules.restaurant import Restaurant, RestaurantModel, ReviewModel, RestaurantCreate, Settings
from user_modules.user_model import User
from mock_data.mock_users_db import USER_DB
import logging
import bcrypt

settings = Settings()
# Passlib context for hashing passwords
pwd_context = bcrypt.hashpw

# Create engines for the primary and secondary databases
primary_engine = create_engine(settings.primary_database_url, pool_pre_ping=True)
PrimarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=primary_engine)

secondary_engine = create_engine(settings.secondary_database_url, pool_pre_ping=True)
SecondarySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=secondary_engine)

Base = declarative_base()
Base.metadata.create_all(bind=primary_engine)

# Create a FastAPI instance
app = FastAPI()

def get_db():
    db = PrimarySessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_secondary_db():
    db = SecondarySessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
# db_config = {
#     'host': os.getenv('DB_HOST'),
#     'dbname': os.getenv('DB_NAME'),
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'port': os.getenv('DB_PORT'),
# }
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
    
#* ----------- User CRUD REST APIs and Authentication ------------###
""" create new User """
# TODO: Create REST API to create new user.
def create_user(user_data, db: Session = Depends(get_db)):
    db_user = User(username=user_data.username, email=user_data.email, hashed_password=user_data.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

""" Authenticate Existing User """
@app.post("/api/authenticate/")
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# @app.post("/api/authenticate/")
# async def authenticate(db, credentials: UserCredentials):
#     user = authenticate_user(db, credentials.username, credentials.password)
#     if user:
#         return {"message": "Authentication successful!", "user": user}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid username or password")
    
    
# @app.post("/api/authenticate/")
# async def authenticate(db, credentials: UserCredentials):
    # user = authenticate_user(db, credentials.username, credentials.password)
    # if user:
    #     return {"message": "Authentication successful!", "user": user}
    # else:
    #     raise HTTPException(status_code=401, detail="Invalid username or password")
    
""" Update Existing User """
# TODO: Create REST API to edit an existing users properties/settings.

#* ------------- Restaurant CRUD REST APIs ---------------------- ###

""" Creates a new restaurant """
@app.post("/api/new_restaurant")
def create_restaurant(restaurant_data: RestaurantCreate, db: Session = Depends(get_db)):
    try:
        db_restaurant = Restaurant(**restaurant_data.model_dump())
        db.add(db_restaurant)
        db.commit()
        db.refresh(db_restaurant)
        return JSONResponse(content={"message": "Restaurant created successfully!"})
    except SQLAlchemyError as e:
        print("Error creating restaurant: ", e)
        raise HTTPException(status_code=500, detail="Database transaction failed")
    finally:
        db.close()
        
""" Returns the entire list of restaurants or return restaurants based on name parameter """
@app.get("/api/restaurants", response_model=list[RestaurantModel])
def get_restaurants(name: Optional[str] = None, skip: int = 0, limit: int = 150, db: Session = Depends(get_db)):
    logging.info(f"Querying restaurants with name: {name}, skip: {skip}, limit: {limit}")
    query = db.query(Restaurant)
    try:
        if not name:
            restaurants = query.offset(skip).limit(limit).all()
            if restaurants:
                return [RestaurantModel.model_validate(restaurant) for restaurant in restaurants]
            else:
                raise HTTPException(status_code=404, detail="Restaurant not found")
        if name:
            query = query.filter(Restaurant.name.ilike(f"%{name}%"))
        restaurants = query.offset(skip).limit(limit).all()
        if restaurants:
            return [RestaurantModel.model_validate(restaurant) for restaurant in restaurants]
        else:
            raise HTTPException(status_code=404, detail="Restaurant not found")
    except SQLAlchemyError as e:
        print("Error fetching restaurants: ", e)
        raise HTTPException(status_code=500, detail="Restaurant not found")
    finally:
        db.close()

""" Returns the restaurant with the matching name """
@app.get("/api/restaurants_by_name/{name}", response_model=list[RestaurantModel])
def get_restaurants_by_name(name: str, db: Session = Depends(get_db)):
    try:
        restaurants = db.query(Restaurant).filter(Restaurant.name.ilike(f"%{name}%")).all()
        if restaurants:
            return [RestaurantModel.model_validate(restaurant) for restaurant in restaurants]
        else:
            raise HTTPException(status_code=404, detail="Restaurant not found")
    except SQLAlchemyError as e:
        print("Error fetching restaurants: ", e)
        raise HTTPException(status_code=500, detail="Error fetching restaurants")  
    finally:
        db.close()

""" Returns the restaurant with the specified ID """
@app.get("/api/restaurant/{id}", response_model=RestaurantModel)
def get_restaurant_by_id(id: int, db: Session=(Depends(get_db)) ):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    try:
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return RestaurantModel.model_validate(restaurant)
    except SQLAlchemyError as e:
        print("Error fetching restaurant: ", e)
        raise HTTPException(status_code=500, detail="list index out of range")
    finally:
        db.close()

""" Returns the recommended list of restaurants """
@app.get("/api/restaurants/recommended", response_model=list[RestaurantModel])
def get_recommended_restaurants(db: Session = Depends(get_secondary_db), skip: int = 0, limit: int = 150, recommended: bool = False):
    # Query the database for the recommended restaurants
    try:
        recommended_restaurants = db.query(Restaurant).offset(skip).limit(limit).all()
        if recommended_restaurants:
            return [RestaurantModel.model_validate(restaurant) for restaurant in recommended_restaurants]
        else:
            raise HTTPException(status_code=404, detail="No recommended restaurants found")
    except SQLAlchemyError as e:
        print("Error fetching recommended restaurants: ", e)
        raise HTTPException(status_code=500, detail="Error fetching recommended restaurants")
    finally:
        db.close()
    

""" Updates the restaurant with the specified ID """
@app.patch("/api/update_restaurant/{id}", response_model=RestaurantModel)
def update_restaurant(id: int, updates: RestaurantModel, db: Session = Depends(get_db)):
    try:
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
        if not db_restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        for key, value in updates.model_dump().items():
            setattr(db_restaurant, key, value)
        db.commit()
        db.refresh(db_restaurant)
        return RestaurantModel.model_validate(db_restaurant)
    except SQLAlchemyError as e:
        print("Error updating restaurant: ", e)
        raise HTTPException(status_code=500, detail="Database transaction failed")
    finally:
        db.close()

""" Deletes the restaurant with the specified ID """
# TODO: Consider and define business logic for deleting a restaurant in relation to reviews.
@app.delete("/api/delete_restaurant/{id}")
def delete_restaurant(id: int, db: Session = Depends(get_db)):
    try:
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
        db.delete(db_restaurant)
        db.commit()
        return {"message": "Restaurant deleted successfully"}
    except SQLAlchemyError as e:
        print("Error deleting restaurant: ", e)
        raise HTTPException(status_code=500, detail="Database transaction failed")
    finally:
        db.close()
