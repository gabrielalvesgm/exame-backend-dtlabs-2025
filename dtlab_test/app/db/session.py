from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#POSTGRES URL CONNECTION (env informations needed)
SQLALCHEMY_DATABASE_URL = "postgresql://root:123456@localhost:5432/dtlabdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()
