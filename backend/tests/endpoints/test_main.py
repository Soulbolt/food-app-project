from fastapi.testclient import TestClient
import pytest
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions, declarative_base

# Add the parent directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))
from main import SessionLocal, app, get_db
from user_modules.user_model import Base
from httpx import AsyncClient
from dotenv import load_dotenv

load_dotenv()

# Define the test database URL
# test_database_url = os.getenv("TEST_DATABASE_URL")

test_database_url = "sqlite:///./restaurants.db"

# Create a test database
if test_database_url is not None:
    print("test_database_url: ", test_database_url)
    engine = create_engine(str(test_database_url), connect_args={"check_same_thread": False})
else:
    raise ValueError("Test database URL is not defined.")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    # Create the test database and the test tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: drop the test tables and the test database
    Base.metadata.drop_all(bind=engine)
    # close_all_sessions()

# Define the override_get_db function
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[SessionLocal] = override_get_db
@pytest.fixture()
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# Create a test client for testing
@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    # Overrite the get_db dependency with the test database
    with TestClient(app) as client:
        yield client



# Test create a new restaurant with status code 201
def test_create_restaurant(client):
    new_restaurant = {
        "category": "American",
        "name": "New Test Restaurant",
        "address": "123 Main St",
        "contact_number": "555-555-5555",
        "rating": float(4.5), # Convert Decimal to float for JSON serialization, float(4.5) == 4.5,
    }

    response = client.post("/api/new_restaurant", json=new_restaurant)
    print("data for post: ", response.json()) # Print the response for debugging

    assert response.status_code == 200
    assert response.json() == {"message": "Restaurant created successfully!"}

    # Verify that the restaurant was added to the database
    response = client.get("/api/restaurants")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert new_restaurant["name"] in [r["name"] for r in response.json()]
    assert len(response.json()) == 101

# Test the get_restaurants endpoint with status code 200
async def test_get_all_restaurants(client):
    names = "pizza"
    response = client.get(f"/api/restaurants/{names}")
    
    # Check if the reponse is JSON before attempting to parse it
    if 'application/json' in response.headers.get('content-type', ''):
        data = response.json()
        print("get all response: ", data) # Print the response for debugging
        assert response.status_code == 200
        assert len(data) > 0 # Check if the response is not empty
    else:
        # Handle non-JSON response
        print("Response is not JSON: ", response)
        assert False, "Expected JSON response"

# Test the get_restaurants endpoint with status code 404
async def get_restaurants_not_found(client):
    response = client.get("/api/restaurants/10")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

# Test the get_restaurants_by_name endpoint with status code 200
def test_get_restaurants_by_name(client, name="pizza"):
    response = client.get(f"/api/restaurants_by_name/{name}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) > 0 # Check if the response is not empty

# Test the get_restaurants_by_name endpoint with status code 500
def test_get_restaurants_by_name_not_found(client, name="not found"):
    response = client.get(f"/api/restaurants_by_name/{name}")
    print("data: ", response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}

# Test the get_restaurant_by_id endpoint with status code 200
def test_get_restaurant_by_id(client):
    response = client.get("/api/restaurant/1")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert response.json()["name"] == "The Gourmet Kitchen"

# Test the get_restaurant_by_id endpoint with status code 500
def test_get_restaurant_by_id_not_found(client):
    response = client.get("/api/restaurant/999")
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"} 

# Test the get_recommended_restaurants endpoint with status code 200
def test_get_recommended_restaurants(client):
    response = client.get("/api/restaurants/recommended")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) == 5

# Test the update_restaurant endpoint with status code 200
def test_update_restaurant(client, id=1):
    update_restaurant = {
        "category": "Mexican",
        "name": "The Golden Gate Grill",
        "address": "123 Main St San Francisco, CA 94105",
        "contact_number": "666-666-6667",
        "rating": float(4.7), # Convert Decimal to float for JSON serialization
    }

    response = client.patch(f"/api/update_restaurant/{id}", json=update_restaurant)
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200

    # Verify that the restaurant was updated in the database
    response = client.get(f"/api/restaurant/{id}")
    print("data validation: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert response.json()["name"] == update_restaurant["name"]

# Test the delete_restaurant endpoint with status code 200
def test_delete_restaurant(client, id=103):
    response = client.delete(f"/api/delete_restaurant/{id}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert response.json() == {"message": "Restaurant deleted successfully"}

    # Verify that the restaurant was deleted from the database
    response = client.get(f"/api/restaurant/{id}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 500
    assert response.json() == {"detail": "list index out of range"}
