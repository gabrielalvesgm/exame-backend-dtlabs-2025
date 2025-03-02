#JWT CONFIGURATION # app/core/security.py

from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
import bcrypt



#Secret key that will be used for encoding and decoding JWT tokens
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hash of the plain password.
    """
    salt = bcrypt.gensalt() #generates a salt and hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8') #return the password as a utf-8 String


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain password matches the bcrypt hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    
def create_access_token(data: dict, expires_delta: Union[timedelta, None]= None) -> str:
    """
    Create a JWT access token with an expiration time.
    """
    to_encode = data.copy()
    #Token expirantion time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expired = datetime.now(timezone.utc) + timedelta(minute=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode a JWT token and return its payload.
    Returns an empty dict if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {}
    except jwt.InvalidTokenError:
        # Token is invalid
        return {}
        
