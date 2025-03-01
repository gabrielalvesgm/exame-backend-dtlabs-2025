#PYDANTIC SCHEMA FOR DATAS
#app/schemas/data.py

from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

#Creating a SensorDataBase class that inherits BaseModel class
class SensorDataBase(BaseModel):
    server_ulid: str                  #Unique identifier (USES BASE32)
    timestamp: datetime               #could be a String aswell / ISO 8601
    temperature: Optional[float] = None #Temperature in celsius
    humidity: Optional[float] = None #Humidity in percentage
    voltage: Optional[float] = None  #Voltage in volts
    current: Optional[float] = None  #Current in ampere
    
    
    #Validation to m.s. that at least one sensor is provided
    @model_validator(mode="after")
    def check_at_least_one_sensor(self):
        sensors = [self.temperature, self.humidity, self.voltage, self.current]
        if all(value is None for value in sensors):
            raise ValueError("At least one sensor value must be provided.")
        return self  #return the instance itself
    
    #end of validation.
    
#Schema to create a sensor data (USED IN POST /data method)
class SensorDataCreate(SensorDataBase):
    pass


#Schema for returning sensor data in responses
class SensorDataResponse(SensorDataBase):
    id: int
    
    class Config:
        from_attributes = True #Enable commpatibility with ORM Objects