from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base
from app.database import engine
from app.database import SessionLocal
from app import models
from app import schemas
from typing import List

app = FastAPI()


@app.on_event("startup")
def startup_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successful.")

        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")

    except Exception as error:
        print("Database connection failed.")
        print(error)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/assets", response_model=schemas.AssetResponse)
def create_asset(asset: schemas.AssetCreate):
    db: Session = SessionLocal()

    new_asset = models.Asset(
        name=asset.name,
        asset_type=asset.asset_type,
        environment=asset.environment,
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    db.close()

    return new_asset


@app.get("/assets", response_model=List[schemas.AssetResponse])
def list_assets():
    db: Session = SessionLocal()

    assets = db.query(models.Asset).all()

    db.close()

    return assets
