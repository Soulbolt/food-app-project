from datetime import datetime, timedelta
import secrets
import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from database_models.base_settings import Settings
from database_models.restaurant_model import Restaurant
from database_models.review_model import Review  # noqa This import is necessary for the database to be created as is expected by the ORM
from database_models.user_model import User
from passlib.hash import bcrypt
from jose import JWTError, jwt
from dotenv import load_dotenv
import logging

from pydantic_models.restaurant_create_and_update_schema import RestaurantCreate
from pydantic_models.restaurant_schema import RestaurantModel
from pydantic_models.user_create_and_credentials_schema import UserCreateModel, UserCredentials

load_dotenv()

settings = Settings()
# Passlib context for hashing passwords
pwd_context = bcrypt.using(rounds=10)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
secret_key = os.getenv("SECRET_KEY")
TIME_EXPIRES = os.getenv("TIME_EXPIRES")

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

#* --------------- Password Hashing, Verification, authenticaiton and token access  ---------------------- ###
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    if secret_key is not None:
        encoded_jwt = jwt.encode(to_encode, secret_key)
    else:
        raise ValueError("secret_key is not specified in the settings.")
    return encoded_jwt

""" Password reset token and email """
def generate_password_reset_token():
    # Generate a secure token.
    password_reset_token = secrets.token_urlsafe()
    return password_reset_token

def send_reset_password_email(email: str, token: str):
    # TODO Implement a function to send an email to the user with the token
    # Send the email with the token to the user
    print(f"Reset password email sent to {email} with token")

#* --------------- Password Reset REST APIs ---------------------- ###
@app.patch("/api/password_rest_request/")
def password_reset_request(email: EmailStr, db: Session = Depends(get_db)):
    # Generate a new token
    new_token = generate_password_reset_token()
    # Query the database for the user with the specified email
    query_result = db.query(User).filter(User.email == email ) \
    .update({"token": new_token, "time_expired": datetime.now() + timedelta(minutes=5)} )
    if not query_result:
        raise HTTPException(status_code=404, detail="User not found")
    # Store the token and its expiration time in the database associated with the user
    db.commit()
    send_reset_password_email(email, new_token)
    return {"message": "Password reset email sent. expires in 5 minutes"}

@app.patch("/api/password_reset/")
def password_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User)
    user_pw_rest = user.filter(User.token == token).first()
    if not user_pw_rest:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the token has expired
    if user_pw_rest.time_expired <= datetime.now(): # type: ignore
        raise HTTPException(status_code=400, detail="Token expired")
    # Update the user's password
    hashed_password = get_password_hash(new_password)
    # Remove the token and its expiration time
    user.filter(user_pw_rest.token == token).update({"password": hashed_password, "token": None, "time_expired": None})
    db.commit()
    return {"message": "Password reset successful"}

#* ----------- User CRUD REST APIs and Authentication ------------###
""" create new User """
@app.post("/api/new_user")
def create_user(user_data: UserCreateModel, db: Session = Depends(get_db)):
    # Hash the password before storing it in the database
    hashed_password = get_password_hash(user_data.hash_password)
    # Add the user to the database
    db_user = User(username=user_data.username, email=user_data.email, password=hashed_password, name=user_data.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return JSONResponse(content={"message": "User created successfully!"})

""" User Login """
@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    if not TIME_EXPIRES:
        raise ValueError("TIME_EXPIRES must be set in .env file")
    
    access_token_expires = timedelta(minutes=float(TIME_EXPIRES))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
    
""" Update Existing User """
# Updates user's name (For now)
@app.patch("/api/update_user/{id}")
def update_user(id: int, name: str, db: Session = Depends(get_db)):
    # Query the database for the user with the specified ID
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update the user's name
    db.query(User).filter(User.id == id).update({"name": name})
    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully!"}

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
def get_recommended_restaurants(db: Session = Depends(get_secondary_db), skip: int = 0, limit: int = 150):
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
