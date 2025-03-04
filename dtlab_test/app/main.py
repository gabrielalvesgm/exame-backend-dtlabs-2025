from fastapi import FastAPI
from app.api.routes import auth, servers, data, health  #Importing routes
from app.db.session import engine, Base
from sqlalchemy import inspect
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    if not existing_tables:
        Base.metadata.create_all(bind=engine)

    yield

app = FastAPI(lifespan=lifespan)

#Include the authentication routes under the "/auth" prefix
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# nclude the server routes under the "/servers" prefix
app.include_router(servers.router, prefix="/servers", tags=["Servers"])

#Include the sensor data routes under the '/data' prefix
app.include_router(data.router, prefix="/data", tags=["Sensor Data"])

#Include the server health routes under the "/health" prefix
app.include_router(health.router, prefix="/health", tags=["Health"])

#Custom OpenAPI Security Schema Configuration
from fastapi.openapi.models import SecurityScheme
from typing import Dict, Any

original_openapi = app.openapi

def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = original_openapi()

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi
