#BUSINESS LOGIC FOR AUTHENTICATION #/app/services/auth_service.py

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.users import UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password

#ENDPOINTS FOR AUTHENTICATION


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.
    The user's password is hashed using bcrypt before storing.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_user_by_username(db: Session, username: str):
    """
    Get a a user from the database based on username.
    """
    normalized_username = username.lower()
    return db.query(models.User).filter(func.lower(models.User.username) == normalized_username).first()



def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate a user by verifying username and password ''match''
    Returns the user if its successful, otherwise, returns False.
    """
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
    