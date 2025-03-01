#MAIN APPLICATION #/app/main.py

from fastapi import FastAPI
from app.api.routes import auth, servers #Importing authentication and server routes.
from app.db.session import engine, Base


app = FastAPI()


#  AUTOMATICALLY CREATES ALL TABLES IN DATABASE IF THEY DONT EXIST.
#  @app.on_event("startup")
#  def on_startup():
#    Base.metadata.create_all(bind=engine)


# Include the authentication routes under the "/auth" prefix
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


# Include the server routes under the "/servers" prefix
app.include_router(servers.router, prefix="/servers", tags=["Servers"])
