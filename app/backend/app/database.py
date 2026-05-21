from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Define how to connect to PostgreSQL
DATABASE_URL = "postgresql+psycopg://vulmp:vulmp_password@postgres:5432/vulmp_db"

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
