from user_modules.user_model import User, Favorite
from restaurant_modules.restaurant import Review

USER_DB: list[User] = [
    User(
        id=1,
        email="admin_rights@owner.com",
        password="immortalknight!",
        username="admin",
        name="Cesar C.",
        favorites=[
            Favorite(
                category= "Italian",
                name= "The Gourmet Kitchen",
                address= "123 Maple Street, Springfield, IL 62704",
                contact_number= "(217) 555-1234",
                rating= 4.5,
                is_favorite= True,
                reviews= [
                    Review(
                        username="foodie123",
                        review="Amazing food and great ambiance!",
                        rating=5
                    ),
                    Review(
                        username="janedoe",
                        review="Good selection, but a bit pricey.",
                        rating=4
                    )
                ]
            ),
            Favorite(
                category= "American",
                name= "The Burger Joint",
                address= "123 Bacon Street, San Francisco, CA 94215",
                contact_number= "(2623) 535-1234",
                rating= 4.5,
                is_favorite= True,
                reviews= [
                    Review(
                        username="foodie123",
                        review="Amazing food and great ambiance!",
                        rating=5
                    ),
                    Review(
                        username="janedoe",
                        review="Good selection, but a bit pricey.",
                        rating=4
                    )
                ]
            ),
        ]
    ),
    User(
        id=2,
        email="user_rights@user.com",
        password="ImUser",
        username="user",
        name="Random user",
        favorites=[
            Favorite(
                category="American",
                name="The Burger Joint",
                address="123 Bacon Street, San Francisco, CA 94215",
                contact_number="(2623) 535-1234",
                rating=4.5,
                is_favorite=True,
                reviews=[
                    Review(
                        username="foodie123",
                        review="Amazing food and great ambiance!",
                        rating=5
                    ),
                    Review(
                        username="janedoe",
                        review="Good selection, but a bit pricey.",
                        rating=4
                    )
                ]
            ),
        ]
    ),
]