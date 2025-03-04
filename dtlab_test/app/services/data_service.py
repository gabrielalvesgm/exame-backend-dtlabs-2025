#BUSINESS LOGIC FOR DATAS #app/services/data_service.py

from sqlalchemy.orm import Session
from app.db import models
from app.schemas.data import SensorDataCreate
from datetime import timezone


def register_sensor_data(db: Session, data: SensorDataCreate):
    sensor_data = models.SensorData(
        server_ulid=data.server_ulid,
        timestamp=data.timestamp.astimezone(timezone.utc),
        temperature=data.temperature,
        humidity=data.humidity,
        voltage=data.voltage,
        current=data.current
    )
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data