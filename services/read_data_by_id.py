from models.sensor_data_model import SensorData
from sqlalchemy import select





async def read_data_by_id(id, session) -> SensorData:

    result = await session.execute(select(SensorData).where(SensorData.id == id))
    existing_data = result.scalar_one_or_none()

    if not existing_data:
        raise ValueError('Row data not found')
    
    return existing_data
