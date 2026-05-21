from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    environment = Column(String, nullable=False)
