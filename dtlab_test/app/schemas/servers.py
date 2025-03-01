#PYDANTIC SCHEMA FOR SERVERS #app/schemas/servers.py

from pydantic import BaseModel
from typing import Optional

#Base Schema for a server
class ServerBase(BaseModel):
    server_name: str
    

#Schema to create a server (used in POST /servers method)
class ServerCreate(ServerBase):
    pass


#Schema to update a server
class ServerUpdate(BaseModel):
    server_name: Optional[str] = None


#Schema for returning the server data (includes ULID generated)
class ServerResponse(ServerBase):
    server_ulid: str
    
    class Config:
        from_attributes = True