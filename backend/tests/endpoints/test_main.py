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

    
