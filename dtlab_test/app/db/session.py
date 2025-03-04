from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL  # importe a variável

engine = create_engine(
    DATABASE_URL,
    future=True,
    connect_args={"options": "-c timezone=utc"}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()