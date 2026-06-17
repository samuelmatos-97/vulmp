import os

from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Define how to connect to PostgreSQL
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ["POSTGRES_HOST"],
    port=int(os.environ["POSTGRES_PORT"]),
    database=os.environ["POSTGRES_DB"],
)

# Create connections to the database
engine = create_engine(DATABASE_URL)

# Allows to open DB sessions, queries, commits, and transactions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create ORM (Object-Relational Mapping) models
Base = declarative_base()

def get_db():
    # Opens a database session
    db = SessionLocal()

    try:
        # Deliver the database session to the endpoint
        yield db
    # Assures that the database session is closed
    finally:
        db.close()
