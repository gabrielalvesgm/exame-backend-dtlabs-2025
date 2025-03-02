#BASE REPOSITORY FOR SQLALCHEMY #app/db/repository.py

from sqlalchemy.orm import Session
import ulid #Lib to generate an ULID for servers
from app.db.models import Server
from app.schemas.servers import ServerCreate, ServerUpdate

#CRUDS SESSION USING SQLALCHEMY ORM

#Creates a new server entity, generating an ULID for a server_ulid
def create_server(db: Session, server_data: ServerCreate):
    new_server = Server(
        server_ulid=str(ulid.new()),
        server_name=server_data.server_name,
    )
    db.add(new_server) #adds new_server to database
    db.commit() #commits 
    db.refresh(new_server)
    return new_server

#SEARCH AN SERVER BY ULID
def get_server_by_ulid(db: Session, server_ulid: str):
    return db.query(Server).filter(Server.server_ulid == server_ulid).first()


#UPDATES AN VALID SERVER DATA
def update_server(db: Session, server_ulid: str, server_data: ServerUpdate):
    db_server = db.query(Server).filter(Server.server_ulid == server_ulid).first()
    if db_server:
        for key, value in server_data.model_dump(exclude_unset=True).items():
            setattr(db_server, key, value)
        db.commit()
        db.refresh(db_server)
    return db_server


#DELETE A SERVER BY ULID
def delete_server(db: Session, server_ulid: str):
    db_server = db.query(Server).filter(Server.server_ulid == server_ulid).first()
    if db_server:
        db.delete(db_server)
        db.commit()
    return db_server