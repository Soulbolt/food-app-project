import pytest
import os
import sys
# Add the parent directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))
from main import app, connect_to_database
from mock_data.mock_restaurants_db import DB
from fastapi.testclient import TestClient

# Override the connect_to_database function to return an in-memory database
def override_connect_to_database():
    return DB

app.dependency_overrides[connect_to_database] = override_connect_to_database

# Create a client for testing
@pytest.fixture
def client():
    return TestClient(app)

# Connect to the mock database
# @pytest.fixture
# def connection():
#     conn = sqlite3.connect(DB) # In-memory database for testing
#     yield conn
#     conn.close()

# Test the get_restaurants endpoint with status code 200
def test_get_all_restaurants(client):
    response = client.get("/api/restaurants")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) > 0 # Check if the response is not empty

# Test the get_restaurants endpoint with status code 404
def test_get_restaurants_not_found(client):
    response = client.get("/api/restaurants")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}

# Test the get_restaurants_by_name endpoint with status code 200
def test_get_restaurants_by_name(client, name="golden"):
    response = client.get(f"/api/restaurants_by_name/{name}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) > 0 # Check if the response is not empty

# Test the get_restaurants_by_name endpoint with status code 500
def test_get_restaurants_by_name_not_found(client, name="golden"):
    response = client.get(f"/api/restaurants_by_name/{name}")
    print("data: ", response.json())
    assert response.status_code == 500
    assert response.json() == {"detail": "500: Restaurant not found"}

# Test the get_restaurant_by_id endpoint with status code 200
def test_get_restaurant_by_id(client):
    response = client.get("/api/restaurant/1")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert response.json()["name"] == "The Golden Gate Grill"

# Test the get_restaurant_by_id endpoint with status code 500
def test_get_retaurant_by_id_not_found(client):
    response = client.get("/api/restaurant/101")
    print(response.json())
    assert response.status_code == 500
    assert response.json() == {"detail": "list index out of range"} 

# Test the get_recommended_restaurants endpoint with status code 200
def test_get_recommended_restaurants(client):
    response = client.get("/api/restaurants/recommended")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) > 0
