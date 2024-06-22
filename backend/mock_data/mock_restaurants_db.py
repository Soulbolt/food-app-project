# Mock database in json format
DB: list[Restaurant] = [{
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
                "username": "pizzalover",
                "review": "Best pizza in town! Highly recommend the Margherita.",
                "rating": 5
            },
            {
                "username": "johnsmith",
                "review": "Great pizza but the service was slow.",
                "rating": 4
            }
        ]
    },
{
        "id": 3,
        "name": "Sushi World",
        "address": "789 Oak Street, Springfield, IL 62706",
        "contact_number": "(217) 555-9012",
        "rating": 4.3,
        "reviews": [
            {
                "username": "sushifan",
                "review": "Fresh sushi and friendly staff.",
                "rating": 5
            },
            {
                "username": "michelles",
                "review": "Good sushi but portions are small.",
                "rating": 4
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
    }]