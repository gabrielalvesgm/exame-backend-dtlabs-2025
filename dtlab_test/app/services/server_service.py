#BUSINESS LOGIC FOR SERVERS #app/services/server.py

from sqlalchemy.orm import Session
from app.db import repository, models
from app.schemas.servers import ServerCreate, ServerUpdate


#Service function to create a new server. (Calls the repo.func. to insert a new server in db)
def create_server_service(db: Session, server_data: ServerCreate):
    return repository.create_server(db, server_data)


#Service function to retrieve a server by ULID
def get_server_by_ulid_service(db: Session, server_ulid: str):
    return repository.get_server_by_ulid(db, server_ulid)

#Service function to list all servers
def list_all_servers_service(db: Session):
    return db.query(models.Server).all()


# Service function to update an valid server
def update_server_service(db: Session, server_ulid: str, server_data: ServerUpdate):
    return repository.update_server(db, server_ulid, server_data)


# Service function to delete an server by ulid
def delete_server_service(db: Session, server_ulid: str):
    return repository.delete_server(db, server_ulid)
