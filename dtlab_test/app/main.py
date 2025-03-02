#MAIN APPLICATION #/app/main.py

from fastapi import FastAPI
from app.api.routes import auth, servers, data, health #Importing routes
from app.db.session import engine, Base

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Drop all tables and recreate them (for development only)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

#@asynccontextmanager
#async def lifespan(app: FastAPI):
    # Startup: Drop and recreate tables (for development/testing only)
#    Base.metadata.drop_all(bind=engine)
#    Base.metadata.create_all(bind=engine)
#    yield


# Include the authentication routes under the "/auth" prefix
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

#Include the server routes under the "/servers" prefix
app.include_router(servers.router, prefix="/servers", tags=["Servers"])

#Include the sensor data routes under the '/data' perfix
app.include_router(data.router, prefix="/data", tags=["Sensor Data"])

#Include the server health routes under the "/health" prefix
app.include_router(health.router, prefix="/health", tags=["Health"])