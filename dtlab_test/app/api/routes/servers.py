from fastapi import APIRouter, Depends, HTTPException, status
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
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

#Dependency to obtain a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Dependency to get the current user token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return username


@router.post("/", response_model=ServerResponse)
def create_server(
    server: ServerCreate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    """
    Create a new server.
    Requires JWT authentication.
    """
    return create_server_service(db, server)



@router.get("/list", response_model=List[ServerResponse])
def list_servers(db: Session = Depends(get_db)):
    """
    List all servers.
    """
    return list_all_servers_service(db)



@router.get("/{server_ulid}", response_model=ServerResponse)
def get_server(server_ulid: str, db: Session = Depends(get_db)):
    """
    Get server details by ULID.
    """
    db_server = get_server_by_ulid_service(db, server_ulid)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server



@router.put("/{server_ulid}", response_model=ServerResponse)
def update_server(server_ulid: str, server: ServerUpdate, db: Session = Depends(get_db)):
    """
    Update server data.
    """
    db_server = update_server_service(db, server_ulid, server)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server



@router.delete("/{server_ulid}", response_model=ServerResponse)
def delete_server(server_ulid: str, db: Session = Depends(get_db)):
    """
    Delete a server.
    """
    db_server = delete_server_service(db, server_ulid)
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server
