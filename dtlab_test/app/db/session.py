# POSTGRES CONNECTION #app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#POSTGRES URL CONNECTION (env informations needed)
SQLALCHEMY_DATABASE_URL = "postgresql://root:123456@localhost:5432/dtlabdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, build=engine)

#Declarative base for models
Base = declarative_base()