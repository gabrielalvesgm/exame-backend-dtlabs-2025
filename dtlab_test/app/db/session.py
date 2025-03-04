from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# POSTGRES URL CONNECTION (replace with your credentials)
SQLALCHEMY_DATABASE_URL = "postgresql://root:123456@localhost:5432/dtlabdb"

# Force the timezone to UTC by using connect_args
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    connect_args={"options": "-c timezone=utc"}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()
