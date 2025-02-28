from fastapi import FastAPI
from app.api.routes.data import router as data_router
from fastapi.testclient import TestClient

app = FastAPI()

app.include_router(data_router, prefix="/data")