#PYDANTIC SCHEMA FOR USERS# app/schemas/users.py

from pydantic import BaseModel, EmailStr


#Schema for create a new user (register)
class UserCreate(BaseModel):
    username: str #User name in register
    email: EmailStr #User email in register
    password: str #Plain password that will be hashed before storing
    

#Schema for user login
class UserLogin(BaseModel):
    username: str #Username for login
    password: str #Password for login (plain)
    

#Schema for returning user data (excluding sensitive fields)
class UserResponse(BaseModel):
    id: int #User ID
    username: str #Username
    email: EmailStr #Email adress of this user
    
    class Config:
        from_attributes = True