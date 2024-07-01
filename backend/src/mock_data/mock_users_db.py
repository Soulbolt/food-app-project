from user_modules.user_model import User

USER_DB: list[User] = [
    {
        "id": 1,
        "email": "admin_rights@owner.com",
        "password": "immortalknight!",
        "username": "admin",
        "name": "Cesar C.",
        "favorites": [
            {
                "category": "Italian",
                "name": "The Gourmet Kitchen",
                "address": "123 Maple Street, Springfield, IL 62704",
                "contact_number": "(217) 555-1234",
                "rating": 4.5,
                "is_favorite": True,
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
                "category": "American",
                "name": "The Burger Joint",
                "address": "123 Bacon Street, San Francisco, CA 94215",
                "contact_number": "(2623) 535-1234",
                "rating": 4.5,
                "is_favorite": True,
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
        ]
    },
    {
        "id": 2,
        "email": "user_rights@user.com",
        "password": "ImUser",
        "username": "user",
        "name": "Random user",
        "favorites": [
            {
                "category": "American",
                "name": "The Burger Joint",
                "address": "123 Bacon Street, San Francisco, CA 94215",
                "contact_number": "(2623) 535-1234",
                "rating": 4.5,
                "is_favorite": True,
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
        ]
    },
]