import pytest
import sqlite3
import os
import sys
# Add the parent directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))
from main import app, connect_to_database
from mock_data.mock_restaurants_db import DB
from fastapi.testclient import TestClient

# Mock database in json format
db = DB

# Override the connect_to_database function to return an in-memory database
def override_connect_to_database():
    conn = sqlite3.connect(DB, uri=True)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()

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
    mock_db = client.app.state.database = {"restaurants": db}
    if mock_db:
        response = client.get("/api/restaurants")
        print(response.json())
        assert response.status_code == 200
        assert len(response.json()) > 0

# Test the get_restaurants endpoint with status code 404
def test_get_restaurants_not_found(client):
    mock_db = client.app.state.database = {"restaurants": []}
    if not mock_db:
        raise Exception("Could not connect to the database")
    response = client.get("/api/restaurants")
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}

# Test the get_restaurants_by_name endpoint with status code 200
def test_get_restaurants_by_name(client):
    response = client.get("/api/restaurants_by_name/golden")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test the get_restaurants_by_name endpoint with status code 404
def test_get_restaurants_by_name_not_found(client, name="not_found"):
    response = client.get(f"/api/restaurants_by_name/{name}")
    data = response.json()
    print(data)
    if response == []:
        assert response.status_code == 404
        assert response.json() == {"detail": "Restaurant not found"}

# Test the get_restaurant_by_id endpoint with status code 200
def test_get_restaurant_by_id(client):
    response = client.get("/api/restaurant/1")
    assert response.status_code == 200
    assert response.json()["name"] == "The Golden Gate Grill"

# Test the get_recommended_restaurants endpoint with status code 200
def test_get_recommended_restaurants(client):
    response = client.get("/api/restaurants/recommended")
    assert response.status_code == 200
    assert len(response.json()) > 0
