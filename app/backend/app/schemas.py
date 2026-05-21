from pydantic import BaseModel


class AssetCreate(BaseModel):
    name: str
    asset_type: str
    environment: str


class AssetResponse(AssetCreate):
    id: int

    class Config:
        from_attributes = True
