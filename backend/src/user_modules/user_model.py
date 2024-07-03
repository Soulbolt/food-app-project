from pydantic import BaseModel
from restaurant_modules.restaurant import Restaurant, Review

""" Pydantic model for User data and Favorites """
class Favorite(BaseModel):
    category: str
    name: str
    address: str
    contact_number: str
    rating: float
    is_favorite: bool
    reviews: list[Review] = []

class User(BaseModel):
    id: int
    email: str
    password: str
    username: str
    name: str
    favorites: list[Favorite] = []

class UserCredentials(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str
    class Config:
        from_attributes = True

class UserInResponse(BaseModel):
    id: int
    email: str
    username: str
    name: str
    favorites: list[Favorite]
    class Config:
        from_attributes = True

class UserInResponseWithToken(UserInResponse):
    access_token: str
    token_type: str
    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    email: str
    password: str
    username: str
    name: str
    class Config:
        from_attributes = True

class UpdateUser(BaseModel):
    email: str
    password: str
    username: str
    name: str
    class Config:
        from_attributes = True

class UpdateUserPassword(BaseModel):
    password: str
    class Config:
        from_attributes = True

class UpdateUserFavorites(BaseModel):
    favorites: list[Favorite]
    class Config:
        from_attributes = True

# Compare this snippet from backend/src/user_modules/user_service.py:
# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session
# from user_modules.user_model import User, UserCredentials, UserInDB, CreateUser, UpdateUser, UpdateUserPassword, UpdateUserFavorites
# from user_modules.user_repository import UserRepository
# 
# class UserService
#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository
# 
#     def get_user_by_email(self, db: Session, email: str) -> UserInDB:
#         user = self.user_repository.get_user_by_email(db, email)
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
# 
#     def get_user_by_id(self, db: Session, user_id: int) -> UserInDB:
#         user = self.user_repository.get_user_by_id(db, user_id)
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
# 
#     def create_user(self, db: Session, user: CreateUser) -> UserInDB:
#         return self.user_repository.create_user(db, user)
# 
#     def update_user(self, db: Session, user_id: int, user: UpdateUser) -> UserInDB:
#         return self.user_repository.update_user(db, user_id, user)
# 
#     def update_user_password(self, db: Session, user_id: int, user: UpdateUserPassword) -> UserInDB:
#         return self.user_repository.update_user_password(db, user_id, user)
# 
#     def update_user_favorites(self, db: Session, user_id: int, user: UpdateUserFavorites) -> UserInDB:
#         return self.user_repository.update_user_favorites(db, user_id, user)
# Compare this snippet from backend/src/user_modules/user_repository.py:
# from sqlalchemy.orm import Session
# from user_modules.user_model import User, UserInDB, CreateUser, UpdateUser, UpdateUserPassword, UpdateUserFavorites
#
# class UserRepository:
#     def get_user_by_email(self, db: Session, email: str) -> UserInDB:
#         return db.query(User).filter(User.email == email).first()
# 
#     def get_user_by_id(self, db: Session, user_id: int) -> UserInDB:
#         return db.query(User).filter(User.id == user_id).first()
# 
#     def create_user(self, db: Session, user: CreateUser) -> UserInDB:
#         db_user = User(**user.dict())
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user
# 
#     def update_user(self, db: Session, user_id: int, user: UpdateUser) -> UserInDB:
#         db_user = db.query(User).filter(User.id == user_id).first()
#         for key, value in user.dict().items():
#             setattr(db_user, key, value)
#         db.commit()
#         db.refresh(db_user)
#         return db_user
# 
#     def update_user_password(self, db: Session, user_id: int, user: UpdateUserPassword) -> UserInDB:
#         db_user = db.query(User).filter(User.id == user_id).first()
#         db_user.password = user.password
#         db.commit()
#         db.refresh(db_user)
#         return db_user
#
#     def update_user_favorites(self, db: Session, user_id: int, user: UpdateUserFavorites) -> UserInDB:
#         db_user = db.query(User).filter(User.id == user_id).first()
#         db_user.favorites = user.favorites
#         db.commit()
#         db.refresh(db_user)
#         return db_user

