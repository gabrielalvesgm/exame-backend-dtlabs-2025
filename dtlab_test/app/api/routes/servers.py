#SERVERS ENDPOINTS #app/rotes/servers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.servers import ServerCreate, ServerUpdate, ServerResponse
from app.services.server_service import (
    create_server_service,
    get_server_by_ulid_service,
    list_all_servers_service,
    update_server_service,
    delete_server_service,
)

router = APIRouter()

#function to: create a new session with database to be used in a requisition, then close conn.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#Endpoints field

#CREATING A NEW SERVER ENDPOINT.
@router.post("/", response_model=ServerResponse)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    return create_server_service(db, server)


#GET ALL SERVERS
@router.get("/list", response_model=List[ServerResponse])
def list_all_servers(db: Session = Depends(get_db)):
    return list_all_servers_service(db)

#GET SERVER BY ULID ENDPOINT
@router.get("/{server_ulid}", response_model=ServerResponse)
def read_server(server_ulid:str, db:Session = Depends(get_db)):
    db_server = get_server_by_ulid_service(db, server_ulid)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server


#UPDATE SERVERS ENDPOINT
@router.put("/{server_ulid}", response_model=ServerResponse)
def update_server(server_ulid: str, server: ServerUpdate, db:Session=Depends(get_db)):
    db_server = update_server_service(db, server_ulid, server)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server Not Found")
    return db_server


#Endpoint to delete a server
@router.delete("/{server_ulid}", response_model=ServerResponse)
def delete_server(server_ulid:str, db:Session = Depends(get_db)):
    db_server = delete_server_service(db, server_ulid)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server Not Found")
    return db_server