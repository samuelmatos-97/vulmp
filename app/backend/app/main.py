from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.database import engine
from app.database import get_db


# Manage application startup and shutdown events (lifecycle)
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Validate the database connection when the application starts."""

    try:
        # Run a simple query to confirm that PostgreSQL is available.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful.")

    except SQLAlchemyError as error:
        # Prevent the API from starting without its required database.
        raise RuntimeError(
            "Application startup failed: database unavailable."
        ) from error

    # The application starts serving requests after this point.
    yield


# Create FastAPI application instance with lifespan context manager
app = FastAPI(lifespan=lifespan)


# If the endpoint answers, it means the FastAPI process is alive
@app.get("/health")
def health_check():
    """Confirm that the FastAPI process is alive."""

    return {"status": "ok"}


# Checks if PostgreSQL is available and can be connected to.
# If the database is unavailable, it returns a 503 code which means the service exists but it is temporarily unavailable to process traffic.
@app.get("/ready")
def readiness_check():
    """Confirm that the API can communicate with PostgreSQL."""

    try:
        # Validate the database dependency using a lightweight query.
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable.",
        ) from error

    return {"status": "ready"}


@app.post("/assets", response_model=schemas.AssetResponse)
def create_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
):
    """Create and persist a new asset."""

    new_asset = models.Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        environment=asset.environment,
    )

    # Store the new asset and retrieve its generated ID.
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@app.get("/assets", response_model=List[schemas.AssetResponse])
def list_assets(db: Session = Depends(get_db)):
    """Return all assets stored in the database."""

    return db.query(models.Asset).all()
