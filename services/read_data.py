
from sqlalchemy import select
from models.sensor_data_model import SensorData
from typing import Optional
from datetime import datetime


async def read_all_data(
        limit: int,
        offset: int, 
        session,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None
        ):
    

    stmt = select(SensorData).offset(offset).limit(limit)

    if start:
        stmt = stmt.where(SensorData.created_at >= start)
    if end:
        stmt = stmt.where(SensorData.created_at <= end)

    results = await session.execute(stmt)
    existing_data = results.scalars().all()

    return existing_data or []
