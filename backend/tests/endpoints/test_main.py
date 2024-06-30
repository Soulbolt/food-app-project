import pytest
import os
import sys

# Add the parent directory to the sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))
from main import app
from restaurant_modules.restaurant import Restaurant
from fastapi.testclient import TestClient

# Create a test client for testing
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Test create a new restaurant with status code 201
def test_create_restaurant(client):
    new_restaurant: Restaurant = {
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
def test_get_all_restaurants(client):
    response = client.get("/api/restaurants")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) > 0 # Check if the response is not empty

# Test the get_restaurants endpoint with status code 404
def test_get_restaurants_not_found(client):
    response = client.get("/api/restaurants/10")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

# Test the get_restaurants_by_name endpoint with status code 200
def test_get_restaurants_by_name(client, name="golden"):
    response = client.get(f"/api/restaurants_by_name/{name}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) > 0 # Check if the response is not empty

# Test the get_restaurants_by_name endpoint with status code 500
def test_get_restaurants_by_name_not_found(client, name="not found"):
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
    response = client.get("/api/restaurant/999")
    print(response.json())
    assert response.status_code == 500
    assert response.json() == {"detail": "list index out of range"} 

# Test the get_recommended_restaurants endpoint with status code 200
def test_get_recommended_restaurants(client):
    response = client.get("/api/restaurants/recommended")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert len(response.json()) == 5

# Test the update_restaurant endpoint with status code 200
def test_update_restaurant(client, id=1):
    update_restaurant: Restaurant = {
        "category": "Mexican",
        "name": "The Golden Gate Grill",
        "address": "123 Main St San Francisco, CA 94105",
        "contact_number": "666-666-6666",
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
def test_delete_restaurant(client, id=102):
    response = client.delete(f"/api/delete_restaurant/{id}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 200
    assert response.json() == {"message": "Restaurant deleted successfully"}

    # Verify that the restaurant was deleted from the database
    response = client.get(f"/api/restaurant/{id}")
    print("data: ", response.json()) # Print the response for debugging
    assert response.status_code == 500
    assert response.json() == {"detail": "list index out of range"}
