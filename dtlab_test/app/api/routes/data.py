#REGISTER AND DATA CONSULTING ENDPOINTS

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.data import SensorDataCreate, SensorDataResponse
from app.services.data_service import register_sensor_data
from app.db.session import SessionLocal

router = APIRouter()

#Dependency to obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
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
















##GLOBAL LIST TO STORAGE DATA (FOR TESTS)
#data_storage = []


##POST ENDPOINT
#@router.post("/", status_code=200)
#def post_data(sensor_data: SensorData):
#    data_storage.append(sensor_data.model_dump())
#    return {"message": "Data received!", "data": sensor_data.model_dump()}


#@router.get("/", status_code=200)
#def get_data():
#    return {"message": "Data retrieved", "data": data_storage}
