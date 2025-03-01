#PYDANTIC SCHEMA FOR AUTH #app/schemas/auth.py

from pydantic import BaseModel


#Base Schema for user details
class UserBase(BaseModel):
    username: str
    email: str
    

#Schema for user Registration (includes password)
class CreateUser(UserBase):
    password: str
    
    
#Schema for returning user data (excludes "sensitive fields")
class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True
        
    
#Schema for token response(JWT)
class Token (UserBase):
    access_token: str
    token_type: str