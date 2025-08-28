from models.sensor_data_model import SensorData


async def enter_row(data, session):

    try:
    
        new_row = SensorData(hum=data.hum, temp=data.temp)
        session.add(new_row)
        await session.commit()
        await session.refresh(new_row)

        return new_row
    
    except Exception as e:
        await session.rollback()
        raise e


   
