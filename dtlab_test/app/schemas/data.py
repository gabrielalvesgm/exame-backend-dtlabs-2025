#PYDANTIC SCHEMA FOR DATAS
#app/schemas/data.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#Creating a SensorDataBase class that inherits BaseModel class
class SensorDataBase(BaseModel):
    server_ulid: str
    timestamp: datetime               #could be a String aswell
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None
    
    
#Schema to create a sensor data (USED IN POST /data method)
class SensorDataCreate(SensorDataBase):
    pass


#Schema for returning sensor data in responses
class SensorDataResponse(SensorDataBase):
    id: int
    
    class Config:
        orm_mode = True #Enable commpatibility with ORM Objects