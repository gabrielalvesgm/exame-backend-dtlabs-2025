#PYDANTIC SCHEMA FOR DATAS #app/schemas/data.py

from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime, timezone

class SensorDataBase(BaseModel):
    server_ulid: str                  # Unique identifier (uses BASE32)
    timestamp: datetime               # ISO 8601 formatted datetime
    temperature: Optional[float] = None  # Temperature in Celsius
    humidity: Optional[float] = None     # Humidity in percentage
    voltage: Optional[float] = None      # Voltage in volts
    current: Optional[float] = None      # Current in ampere

    @model_validator(mode="after")
    def ensure_timestamp_aware(self):
        if self.timestamp.tzinfo is None:
            self.timestamp = self.timestamp.replace(tzinfo=timezone.utc)
        return self

    #Validate that at least one sensor value is provided
    @model_validator(mode="after")
    def check_at_least_one_sensor(self):
        sensors = [self.temperature, self.humidity, self.voltage, self.current]
        if all(value is None for value in sensors):
            raise ValueError("At least one sensor value must be provided.")
        return self

#Schema to create a sensor data (used in POST /data)
class SensorDataCreate(SensorDataBase):
    pass

#Schema for returning sensor data in responses
class SensorDataResponse(SensorDataBase):
    id: int

#Schema for returning a sensor data query response (with aggregation)
class SensorDataQueryResponse(BaseModel):
    timestamp: datetime
    value: float

    class Config:
        from_attributes = True  #Enable compatibility with ORM objects
