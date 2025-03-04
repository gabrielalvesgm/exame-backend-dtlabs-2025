from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

from app.schemas.data import SensorDataCreate, SensorDataResponse, SensorDataQueryResponse
from app.services.data_service import register_sensor_data
from app.db.session import SessionLocal
from app.db import models
from app.core.security import decode_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency to obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Dependency to get the current user (returns username)
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return username

#SensorData POST endpoint to register a sensor data record
@router.post("/", response_model=SensorDataResponse)
def post_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a sensor data.
    The payload must include a valid server_ulid and at least one sensor value.
    """
    sensor_data = register_sensor_data(db, data)
    if not sensor_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Server not found"
        )
    return sensor_data


#GET /data endpoint to query sensor data with optional filters and aggregation.
@router.get("/")
def query_sensor_data(
    server_ulid: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    sensor_type: Optional[str] = None,
    aggregation: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    allowed_sensors = {"temperature", "humidity", "voltage", "current"}
    allowed_aggregations = {"minute", "hour", "day"}

    if sensor_type is None:
        raise HTTPException(status_code=400, detail="sensor_type query parameter is required")
    if sensor_type not in allowed_sensors:
        raise HTTPException(status_code=400, detail="Invalid sensor_type")
    if aggregation and aggregation not in allowed_aggregations:
        raise HTTPException(status_code=400, detail="Invalid aggregation value")

    query = db.query(models.SensorData)

    if server_ulid:
        query = query.filter(models.SensorData.server_ulid == server_ulid)
    if start_time:
        query = query.filter(models.SensorData.timestamp >= start_time)
    if end_time:
        query = query.filter(models.SensorData.timestamp <= end_time)

    sensor_column = getattr(models.SensorData, sensor_type)

    if aggregation:
        
        truncated = func.date_trunc(aggregation, models.SensorData.timestamp).label("timestamp")
        avg_value = func.avg(sensor_column).label("value")
        results = (
            query.with_entities(truncated, avg_value)
            .group_by(truncated)
            .order_by(truncated)
            .all()
        )
        return [{"timestamp": row.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), sensor_type: row.value} for row in results]
    else:
        results = (
            query.with_entities(models.SensorData.timestamp, sensor_column.label("value"))
            .order_by(models.SensorData.timestamp)
            .all()
        )
        return [{"timestamp": row.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), sensor_type: row.value} for row in results]
