from pydantic import BaseModel
from pydantic import field_validator
from pydantic.json_schema import SkipJsonSchema


class AssetCreate(BaseModel):
    name: str
    asset_type: str
    environment: str


class AssetUpdate(BaseModel):
    """Validate fields provided in a partial asset update."""

    # Allow omitted fields while documenting only string values.
    name: str | SkipJsonSchema[None] = None
    asset_type: str | SkipJsonSchema[None] = None
    environment: str | SkipJsonSchema[None] = None

    @field_validator("name", "asset_type", "environment")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        """Reject null values for explicitly provided fields."""

        if value is None:
            raise ValueError("Field cannot be null.")

        return value


class AssetResponse(AssetCreate):
    id: int

    class Config:
        from_attributes = True
