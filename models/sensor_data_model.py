from config.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func


class SensorData(Base):
    __tablename__ = "sensor_data"
    __table_args__ = {"schema":"public"}

    id = Column(Integer, primary_key=True, index=True)
    temp = Column(Float, nullable=False, index=True)
    hum = Column(Float, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        index=True,
        )