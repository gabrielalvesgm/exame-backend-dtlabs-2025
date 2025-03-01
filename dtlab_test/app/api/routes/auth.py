#AUTHENTICATION ENDPOINTS#app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.users import UserCreate, UserLogin, UserResponse
from app.services.auth_service import create_user, authenticate_user, get_user_by_username
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.session import SessionLocal

router = APIRouter()


#Dependency to obatin a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/register", response_model=UserResponse)
def register(user:UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    Raises an error if the username is already registered.
    """
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    new_user = create_user(db, user)
    return new_user


@router.post("login")
def login(user: UserLogin, db:Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and return a JWT token.
    Raises an error if the username or password is invalid.
    """
    auth_user = authenticate_user(db, user.username, user.password)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )
        #Token Expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": auth_user.username},
        expires_delta=access_token_expires
    )
    return{"access_token": token, "token_type": "bearer"}