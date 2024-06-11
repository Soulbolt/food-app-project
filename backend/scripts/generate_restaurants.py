import random
from faker import Faker
from faker.providers import BaseProvider
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

class CustomPhoneNumberProvider(BaseProvider):
    def phone_number(self):
        formats = ['(###) ###-####', '###-###-####']
        pattern = self.random_element(formats)
        return self.numerify(pattern)
    
load_dotenv()

fake = Faker()
fake.add_provider(CustomPhoneNumberProvider)

categories = [ "Italian", "Chinese", "Mexican", "Indian", "American", "Japanese", "French", "Thai", "Greek", "Mediterranean"]

"""
Generate a list of restaurants with random data.

Args:
    num_restaurants (int): The number of restaurants to generate.

Returns:
    list: A list of tuples, where each tuple contains the category, name, address, contact number, and rating of a restaurant.
"""
def generate_restaurant(num_restaurants):
    restaurants = []

    # Read CSV file
    restaurant_names = []
    with open('restaurant_names.csv', 'r') as file:
        restaurant_names_list = file.readlines()
        for name in restaurant_names_list:
            restaurant_names.append(name.strip())

    for i in range(num_restaurants):
        category = random.choice(categories)
        name = restaurant_names[i].replace("'", '""')
        address = fake.address().replace("\n", ", ").replace("'", "''") # Replace single quotes with two single quotes
        contact_number = fake.phone_number().replace("'", "''") # Replace single quotes with two single quotes
        rating = round(random.uniform(1.0, 5.0), 1)
        restaurants.append((category, name, address, contact_number, rating))
    return restaurants

def generate_reviews(num_reviews):
    reviews = []
    for i in range(num_reviews):
        restaurant_id = random.randint(1, 100)
        username = fake.name().replace("'", "''")
        review = fake.text().replace("\n", ", ").replace("'", "''") # Replace single quotes with two single quotes
        rating = round(random.uniform(1.0, 5.0), 1)
        reviews.append((restaurant_id, username, review, rating))
    return reviews

# Generate 100 random reviews
review_data = generate_reviews(100)
# num_reviews = 100
# reviews = generate_reviews(num_reviews)
# print(reviews)
# Generate 100 random restaurants
restaurant_data = generate_restaurant(100)
# num_restaurants = 100
# restaurants = generate_restaurant(num_restaurants)
# print(restaurants)

# Generate SQL INSERT statements
insert_restaurant_statements = []
insert_review_statements = []
for data in restaurant_data:
    category, name, address, contact_number, rating = data
    insert_restaurant_statements.append(f"INSERT INTO restaurant_schema.restaurants (category, name, address, contact_number, rating) VALUES ('{category}', '{name}', '{address}', '{contact_number}', {rating});")

for data in review_data:
    restaurant_id, username, review, rating = data
    insert_review_statements.append(f"INSERT INTO restaurant_schema.reviews (restaurant_id, username, review, rating) VALUES ({restaurant_id}, '{username}', '{review}', {rating});")

# Write SQL INSERT statements to file, can comment out if file is not needed   
# with open("insert_restaurants.sql", "w") as file:
#     file.write("\n".join(insert_statements))

# print("SQL statements written to insert_restaurants.sql successfully")

# Dabase configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT'),
}

def connect_to_database():
    try:
        print("Connecting to the PostgreSQL database...")
        # Establish connection
        conn = psycopg2.connect(**db_config)
        print("Connected to the database!")
        return conn

    except Exception as e:
        print("Error connecting to PostgreSQL database: ", e)
        return None
    
def insert_restaurants():
    conn = connect_to_database()
    try:
        # Create a cursor object
        cursor = conn.cursor()

        for sql_statement in insert_restaurant_statements:
            cursor.execute(sql_statement)

        conn.commit()
        print("Restaurants inserted successfully")

        for sql_statement in insert_review_statements:
            cursor.execute(sql_statement)

        conn.commit()
        print("Reviews inserted successfully")
    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        print("Error inserting data: ", e)
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Connection to the database closed successfully")


insert_restaurants()
