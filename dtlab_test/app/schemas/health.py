#PYDANTIC SCHEMA FOR HEALTH#app/schemas/health.py

from pydantic import BaseModel

class ServerHealthResponse(BaseModel):
    server_ulid: str
    status: str
    server_name: str