
# from sqlalchemy import select
# from models.sensor_data_model import SensorData
# from typing import Optional
# from datetime import datetime


# async def read_all_data(
#         limit: int,
#         offset: int, 
#         session,
#         start: Optional[datetime] = None,
#         end: Optional[datetime] = None
#         ):
    

#     stmt = select(SensorData).offset(offset).limit(limit)

#     if start:
#         stmt = stmt.where(SensorData.created_at >= start)
#     if end:
#         stmt = stmt.where(SensorData.created_at <= end)

#     results = await session.execute(stmt)
#     existing_data = results.scalars().all()

#     return existing_data or []


from sqlalchemy import select
from models.sensor_data_model import SensorData
from datetime import timezone

async def read_all_data(limit, offset, order="desc", start=None, end=None, session=None):
    if start and getattr(start, "tzinfo", None):
        start = start.astimezone(timezone.utc).replace(tzinfo=None)
    if end and getattr(end, "tzinfo", None):
        end = end.astimezone(timezone.utc).replace(tzinfo=None)

    stmt = select(SensorData)
    if start:
        stmt = stmt.where(SensorData.created_at >= start)
    if end:
        stmt = stmt.where(SensorData.created_at <= end)

    if order == "asc":
        stmt = stmt.order_by(SensorData.created_at.asc(), SensorData.id.asc())
    else:
        stmt = stmt.order_by(SensorData.created_at.desc(), SensorData.id.desc())

    stmt = stmt.offset(offset).limit(limit)

    res = await session.execute(stmt)
    return res.scalars().all() or []