#BUSINESS LOGIC FOR DATAS #app/services/data_service.py

from sqlalchemy.orm import Session
from app.db import models
from app.schemas.data import SensorDataCreate


def register_sensor_data(db: Session, data: SensorDataCreate):
    """
    Register sensor data in the database.
    Verifies if the server exists before inserting data.
    Returns the sensor data record if successful, or None if the server is not found.
    """
    
    #Checking if server is valid by ulid
    server = db.query(models.Server).filter(models.Server.server_ulid == data.server_ulid)
    if not server:
        return None
    
    sensor_data = models.SensorData(
        server_ulid=data.server_ulid,
        timestamp=data.timestamp,
        temperature=data.temperature,
        humidity=data.humidity,
        voltage=data.voltage,
        current=data.current
    )
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data