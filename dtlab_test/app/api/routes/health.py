import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List
from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from app.db import models
from app.core.security import decode_access_token
from app.schemas.health import ServerHealthResponse

#Configure basic logging with timestamp, level and message
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

router = APIRouter()

#OAuth2 scheme to extract the JWT token from the header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Dependency to create a DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get the current user (returns username)
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    logging.debug(f"Authenticated user: {username}")
    return username


# Function to get server status and last sensor timestamp
def get_server_status(db: Session, server_ulid: str) -> dict:
    sensor = (
        db.query(models.SensorData)
        .filter(models.SensorData.server_ulid == server_ulid)
        .order_by(models.SensorData.timestamp.desc())
        .first()
    )
    if sensor:
        sensor_dt = sensor.timestamp
        
        if sensor_dt.tzinfo is None:
            sensor_dt = sensor_dt.replace(tzinfo=timezone.utc)
        else:
            sensor_dt = sensor_dt.astimezone(timezone.utc)
        now = datetime.now(timezone.utc)
        diff = (now - sensor_dt).total_seconds()
        logging.debug(f"Server {server_ulid} - Now: {now.isoformat()}, Sensor: {sensor_dt.isoformat()}, Diff: {diff} seconds")
        status = "online" if diff < 30 else "offline"
        return {"status": status, "last_timestamp": sensor_dt}
    logging.debug(f"Server {server_ulid} - No sensor data; returning offline.")
    return {"status": "offline", "last_timestamp": None}


#GET /health/all (return health status for all servers (of the current user))
@router.get("/all", response_model=List[ServerHealthResponse])
def get_all_servers_health(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    #For testing it return all servers.
    servers = db.query(models.Server).all()
    result = []
    for server in servers:
        status_info = get_server_status(db, server.server_ulid)
        result.append(ServerHealthResponse(
            server_ulid=server.server_ulid,
            status=status_info["status"],
            server_name=server.server_name,
            last_timestamp=status_info["last_timestamp"]
        ))
    return result

#GET /health/{server_ulid} (return the health status of a single server)
@router.get("/{server_ulid}", response_model=ServerHealthResponse)
def get_server_health(
    server_ulid: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    server = db.query(models.Server).filter(models.Server.server_ulid == server_ulid).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    status_info = get_server_status(db, server_ulid)
    return ServerHealthResponse(
        server_ulid=server.server_ulid,
        status=status_info["status"],
        server_name=server.server_name,
        last_timestamp=status_info["last_timestamp"]
    )
