from fastapi import FastAPI
from app.api.routes import servers
from app.db.session import engine, Base

app = FastAPI()

#AUTOMATICALLY CREATES ALL TABLES IN DATABASE IF THEY DONT EXIST.
#@app.on_event("startup")
#def on_startup():
#  Base.metadata.create_all(bind=engine)


app.include_router(servers.router, prefix="/servers", tags=["Servers"])
