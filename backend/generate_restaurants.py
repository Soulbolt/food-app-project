import random
from faker import Faker

fake = Faker()

categories = [ "Italian", "Chinese", "Mexican", "Indian", "American", "Japanese", "French", "Thai", "Greek", "Mediterranean"]

def generate_restaurant(num_restaurants):
    restaurants = []

    for i in range(num_restaurants):
        category = random.choice(categories)
        name = fake.name().replace("'", "''") # Replace single quotes with two single quotes
        address = fake.address().replace("\n", ", ").replace("'", "''") # Replace single quotes with two single quotes
        contact_number = fake.phone_number().replace("'", "''") # Replace single quotes with two single quotes
        rating = round(random.uniform(1.0, 5.0), 1)
        restaurants.append((category, name, address, contact_number, rating))
    return restaurants