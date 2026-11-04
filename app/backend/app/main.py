from contextlib import asynccontextmanager
from typing import Annotated
from typing import List

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Path
from fastapi import Response
from fastapi import status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.database import engine
from app.database import get_db


# Restrict asset IDs to PostgreSQL's signed 32-bit INTEGER range.
AssetId = Annotated[int, Path(ge=-2147483648, le=2147483647)]


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


@app.get("/assets/{asset_id}", response_model=schemas.AssetResponse)
def get_asset(
    asset_id: AssetId,
    db: Session = Depends(get_db),
):
    """Return one asset by its ID."""

    # Find the asset with the requested ID.
    asset = (
        db.query(models.Asset)
        .filter(models.Asset.id == asset_id)
        .first()
    )

    # Return 404 when the asset does not exist.
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found.",
        )

    return asset


@app.patch("/assets/{asset_id}", response_model=schemas.AssetResponse)
def update_asset(
    asset_id: AssetId,
    asset_update: schemas.AssetUpdate,
    db: Session = Depends(get_db),
):
    """Update the provided fields of an existing asset."""

    try:
        # Find the asset with the requested ID.
        asset = (
            db.query(models.Asset)
            .filter(models.Asset.id == asset_id)
            .first()
        )

        if asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
            )

        # Apply only fields explicitly included in the request.
        update_data = asset_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(asset, field, value)

        # Save the changes and reload the stored values.
        db.commit()
        db.refresh(asset)

    except SQLAlchemyError as error:
        # Roll back the active transaction after a database error.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed.",
        ) from error

    return asset


@app.delete(
    "/assets/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_asset(
    asset_id: AssetId,
    db: Session = Depends(get_db),
) -> Response:
    """Delete an asset by its ID."""

    try:
        # Find the asset with the requested ID.
        asset = (
            db.query(models.Asset)
            .filter(models.Asset.id == asset_id)
            .first()
        )

        if asset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found.",
            )

        # Mark the asset for deletion and commit the transaction.
        db.delete(asset)
        db.commit()

    except SQLAlchemyError as error:
        # Roll back the active transaction after a database error.
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed.",
        ) from error

    # Return an empty response after successful deletion.
    return Response(status_code=status.HTTP_204_NO_CONTENT)
