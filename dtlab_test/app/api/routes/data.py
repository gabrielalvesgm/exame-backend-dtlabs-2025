#REGISTER AND DATA CONSULTING ENDPOINTS

from fastapi import APIRouter
from app.schemas.data import SensorData

router = APIRouter()

#GLOBAL LIST TO STORAGE DATA (FOR TESTS)
data_storage = []


#POST ENDPOINT
@router.post("/", status_code=200)
def post_data(sensor_data: SensorData):
    data_storage.append(sensor_data.model_dump())
    return {"message": "Data received!", "data": sensor_data.model_dump()}


@router.get("/", status_code=200)
def get_data():
    return {"message": "Data retrieved", "data": data_storage}
