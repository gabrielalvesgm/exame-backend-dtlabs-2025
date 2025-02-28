#PYDANTIC SCHEMA FOR SERVERS #app/schemas/servers.py

from pydantic import BaseModel

#Base Schema for a server
class ServerBase(BaseModel):
    server_name: str
    

#Schema to create a server (used in POST /servers method)
class ServerCreate(ServerBase):
    pass


#Schema for returning the server data (includes ULID generated)
class ServerResponse(ServerBase):
    server_ulid: str
    
    class Config:
        orm_mode = True