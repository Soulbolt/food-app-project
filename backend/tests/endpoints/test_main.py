import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from restaurant_modules.restaurant import Restaurant


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="module")
def test_read_restaurants(client, db_session):
    for i in range(10):
        restaurant = Restaurant(
            name=f"restaurant_{i}",
            address=f"address_{i}",
            contact_number=f"contact_number_{i}",
            rating=i,
        )
        db_session.add(restaurant)
    db_session.commit()
    yield

    response = client.get("/api/restaurant")
    assert response.status_code == 200
    assert len(response.json()) == 10

@pytest.fixture(scope="module")
def test_read_restaurants_by_name(client, db_session):
    for i in range(10):
        restaurant = Restaurant(
            name=f"restaurant_{i}",
            address=f"address_{i}",
            contact_number=f"contact_number_{i}",
            rating=i,
        )
        db_session.add(restaurant)
    db_session.commit()
    yield

    response = client.get("/api/restaurants_by_name/restaurant_1")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.get("/api/restaurants_by_name/restaurant_5")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/api/restaurants_by_name/restaurant_10")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.get("/api/restaurants_by_name/restaurant")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.get("/api/restaurants_by_name/restaurant_11")
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}

@pytest.fixture(scope="module")
def test_read_restaurants_by_id(client, db_session):
    for i in range(10):
        restaurant = Restaurant(
            name=f"restaurant_{i}",
            address=f"address_{i}",
            contact_number=f"contact_number_{i}",
            rating=i,
        )
        db_session.add(restaurant)
    db_session.commit()
    yield

    response = client.get("/api/restaurant/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "restaurant_0",
        "address": "address_0",
        "contact_number": "contact_number_0",
        "rating": 0,
        "reviews": [],
    }

    response = client.get("/api/restaurant/5")
    assert response.status_code == 200
    assert response.json() == {
        "id": 5,
        "name": "restaurant_4",
        "address": "address_4",
        "contact_number": "contact_number_4",
        "rating": 4,
        "reviews": [],
    }

    response = client.get("/api/restaurant/10")
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}

    response = client.get("/api/restaurant/11")
    assert response.status_code == 404
    assert response.json() == {"detail": "Restaurant not found"}
