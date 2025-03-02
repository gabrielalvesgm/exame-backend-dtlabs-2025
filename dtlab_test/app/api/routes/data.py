#REGISTER AND DATA CONSULTING ENDPOINTS

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer

from app.schemas.data import SensorDataCreate, SensorDataResponse
from app.services.data_service import register_sensor_data
from app.db.session import SessionLocal
from app.db import models
from app.core.security import decode_access_token
from app.schemas.data import SensorDataQueryResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Dependency to obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return username


#SensorData post endpoint to register a sensordata
@router.post("/", response_model=SensorDataResponse)
def post_sensor_data(data: SensorDataCreate, db:Session = Depends(get_db)):
    """
    Endpoint to register a sensor data.
    The payload must include a valid server_ulid and at least one sensor value.
    """
    sensor_data = register_sensor_data(db, data)
    if not sensor_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details="Server not found"
        )
    return sensor_data


@router.get("/", response_model=List[SensorDataResponse])
def query_sensor_data(
    server_ulid: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    sensor_type: Optional[str] = None,
    agreggation: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_db)
):
    #Validate sensor_type and aggregation
    allowed_sensors = {"temperature", "humidity", "voltage", "current"}
    allowed_aggregations = {"minute", "hourd", "day"}
    
    if sensor_type is None:
        raise HTTPException(status_code=400, detail="sensor_type query parameter is required")
    if sensor_type is not allowed_sensors:
        raise HTTPException(status_code=400, detail="Invalid sensor_type")
    if agreggation and agreggation not in allowed_aggregations:
        raise HTTPException(status_code=400, detail="Invalid agreggation value")
    
    #Base query on SensorData
    query = db.query(models.SensorData)
    
    if server_ulid:
        query = query.filter(models.SensorData.server_ulid == server_ulid)
    if start_time:
        query = query.filter(models.SensorData.timestamp >= start_time)
    if end_time:
        query = query.filter(models.SensorData.timestamp <= end_time)
    
    sensor_column = getattr(models.SensorData, sensor_type)
    
    #Using postgres date_trunc function to group by desired interval
    if agreggation:
        truncated = func.date_trunc(agreggation, models.SensorData.timestamp).label("timestamp")
        avg_value = func.avg(sensor_column).label("value")
        results = (
            query.with_entities(truncated, avg_value)
            .group_by(truncated)
            .order_by(truncated)
            .all()
        )
        return[SensorDataQueryResponse(timestamp=row.timestamp, value=row.value) for row in results]
    else:
        results = (
            query.with_entities(models.SensorData.timestamp, sensor_column.label("value"))
            .order_by(models.SensorData.timestamp)
            .all()
        )
        return [SensorDataQueryResponse(timestamp=row.timestamp, value=row.value) for row in results]
        
