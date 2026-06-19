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
from app.database import Base
from app.database import engine
from app.database import get_db


# Manage application startup and shutdown events (lifecycle)
@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful.")

        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")

    except SQLAlchemyError as error:
        print("Application startup failed: database unavailable.")
        # Stops the application from looking functional when a dependency is unavailable
        raise RuntimeError(
            "Application startup failed: database unavailable."
        ) from error

    yield


# Create FastAPI application instance with lifespan context manager
app = FastAPI(lifespan=lifespan)


# If the endpoint answers, it means the FastAPI process is alive
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Checks if PostgreSQL is available and can be connected to.
# If the database is unavailable, it returns a 503 code which means the service exists but it is temporarily unavailable to process traffic.
@app.get("/ready")
def readiness_check():
    try:
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
    new_asset = models.Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        environment=asset.environment,
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@app.get("/assets", response_model=List[schemas.AssetResponse])
def list_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()
