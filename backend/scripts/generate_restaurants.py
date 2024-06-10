import random
from faker import Faker

fake = Faker()

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
        name = restaurant_names[i]
        address = fake.address().replace("\n", ", ").replace("'", "''") # Replace single quotes with two single quotes
        contact_number = fake.phone_number().replace("'", "''") # Replace single quotes with two single quotes
        rating = round(random.uniform(1.0, 5.0), 1)
        restaurants.append((category, name, address, contact_number, rating))
    return restaurants

# Geenerate 100 random restaurants
restaurant_data = generate_restaurant(100)
# num_restaurants = 100
# restaurants = generate_restaurant(num_restaurants)
# print(restaurants)

# Generate SQL INSERT statements
insert_statements = []
for data in restaurant_data:
    category, name, address, contact_number, rating = data
    insert_statements.append(f"INSERT INTO restaurants (category, name, address, contact_number, rating) VALUES ('{category}', '{name}', '{address}', '{contact_number}', {rating});")

# Write SQL INSERT statements to file   
with open("insert_restaurants.sql", "w") as file:
    file.write("\n".join(insert_statements))

print("SQL statements written to insert_restaurants.sql successfully")
