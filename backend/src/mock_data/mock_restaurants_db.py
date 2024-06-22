# Mock database in json format
class DB:
    def __init__(self):
        self.DB = self.generate_mock_db()

    def generate_mock_db(self):
        return [
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
