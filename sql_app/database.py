from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db" -> for PostgreSQL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    # the argument "connect_args" is needed only for SQLite. It's not needed for other databases.
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.

Base = declarative_base()
