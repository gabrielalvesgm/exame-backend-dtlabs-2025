#PYDANTIC SCHEMA FOR HEALTH#app/schemas/health.py

from pydantic import BaseModel
from datetime import datetime

class ServerHealthResponse(BaseModel):
    server_ulid: str
    status: str
    server_name: str
    last_timestamp: datetime | None