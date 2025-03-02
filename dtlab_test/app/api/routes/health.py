#MONITORING ENDPOINTS#/app/api/routes/health.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from typing import List
from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from app.db import models
from app.core.security import decode_access_token
from app.schemas.health import ServerHealthResponse


router = APIRouter()


#OAUTH2 scheme to extract the jwt token from the header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Dependency to create a DB Session
def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
        
        
#Dependency to get the current user (just returns username)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    username = payload.get("dub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return username


#Dependency to get server status (based on 10s coldown)
def get_server_status(db: Session, server_ulid: str) -> str:
    """
    Check the latest sensor data for the server and return "online" if the
    last data is within 10 seconds, otherwise "offline".
    """
    sensor = (
        db.query(models.SensorData)
        .filter(models.SensorData.server_ulid == server_ulid)
        .order_by(models.SensorData.timestamp.desc())
        .first()
    )
    if sensor:
        now = datetime.now(timezone.utc)
        if now - sensor.timestamp <= timedelta(seconds=10):
            return "online"
    return "offline"



#GET /health/all (return health status for all servers (of the current user)
@router.get("/all", response_model=List[ServerHealthResponse])
def get_all_servers_health(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_db)
):
    #Returning all servers for testing purposes
    servers = db.query(models.Server).all()
    result = []
    for server in servers:
        status_str = get_server_status(db, server.server_ulid)
        result.append(ServerHealthResponse(
            server_ulid=server.server_ulid,
            status=status_str,
            server_name=server.server_name
        ))
        return result


    
# GET /health/{server_ulid} (return the health status the current ulid server)
@router.get("/{server_ulid}", response_model=ServerHealthResponse)
def get_server_health(
    server_ulid: str, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    server = db.query(models.Server).filter(models.Server.server_ulid == server_ulid).first()
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    status_str = get_server_status(db, server_ulid)
    return ServerHealthResponse(
        server_ulid=server.server_ulid,
        status=status_str,
        server_name=server.server_name
    )
    


