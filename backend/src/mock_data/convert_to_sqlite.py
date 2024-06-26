import sqlite3

# Mock database in json format
DB = [
    {
        "id": 1,
        "name": "The Gourmet Kitchen",
        "address": "123 Maple Street, Springfield, IL 62704",
        "contact_number": "(217) 555-1234",
        "rating": 4.5,
        "reviews": [
            {
                "username": "foodie123",
                "review": "Amazing food and great ambiance!",
                "rating": 5
            },
            {
                "username": "janedoe",
                "review": "Good selection, but a bit pricey.",
                "rating": 4
            }
        ]
    },
    {
        "id": 2,
        "name": "Pizza Paradise",
        "address": "456 Elm Avenue, Springfield, IL 62705",
        "contact_number": "(217) 555-5678",
        "rating": 4.7,
        "reviews": [
            {
                "username": "sarahjones",
                "review": "The best pizza I've ever had. I love it!",
                "rating": 5
            },
            {
                "username": "johndoe",
                "review": "I had the cheese and tomato pizza.",
                "rating": 3
            }
        ]
    },
    {
        "id": 3,
        "name": "Thai Curry House",
        "address": "789 Oak Road, Springfield, IL 62706",
        "contact_number": "(217) 555-9012",
        "rating": 4.3,
        "reviews": [
            {
                "username": "thaichef",
                "review": "The best curry I've ever had. I love it!",
                "rating": 5
            },
            {
                "username": "johndoe",
                "review": "I had the chicken and rice curry.",
                "rating": 3
            }
        ]
    },
    {
        "id": 4,
        "name": "Curry House",
        "address": "101 Pine Lane, Springfield, IL 62707",
        "contact_number": "(217) 555-3456",
        "rating": 4.6,
        "reviews": [
            {
                "username": "spicylover",
                "review": "Authentic Indian food with the perfect amount of spice.",
                "rating": 5
            },
            {
                "username": "lukewarm",
                "review": "Food was good but service could be better.",
                "rating": 4
            }
        ]
    },
    {
        "id": 5,
        "name": "Burger Barn",
        "address": "202 Birch Road, Springfield, IL 62708",
        "contact_number": "(217) 555-7890",
        "rating": 4.2,
        "reviews": [
            {
                "username": "burgerking",
                "review": "Juicy burgers and crispy fries!",
                "rating": 5
            },
            {
                "username": "anonymouse",
                "review": "Burgers were decent, but the place was crowded.",
                "rating": 3
            }
        ]
    }
]

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('restaurants.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact_number TEXT NOT NULL,
    rating REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant_id INTEGER,
    username TEXT NOT NULL,
    review TEXT NOT NULL,
    rating REAL NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
)
''')

# Insert data into restaurants table
for restaurant in DB:
    cursor.execute('''
    INSERT INTO restaurants (id, name, address, contact_number, rating)
    VALUES (?, ?, ?, ?, ?)
    ''', (restaurant['id'], restaurant['name'], restaurant['address'], restaurant['contact_number'], restaurant['rating']))

    # Insert data into reviews table
    for review in restaurant['reviews']:
        cursor.execute('''
        INSERT INTO reviews (restaurant_id, username, review, rating)
        VALUES (?, ?, ?, ?)
        ''', (restaurant['id'], review['username'], review['review'], review['rating']))

# Commit the changes and close the connection
conn.commit()
conn.close()
