import hmac
from fastapi import APIRouter, Header, Request, status, Depends, HTTPException, Query
from schemas.sensor_data_schema import SensorDataSchemaCreate, SensorDataSchemaRead
from config.db import get_session
from sqlalchemy.ext.asyncio import  AsyncSession
from services.create_row import enter_row
from services.read_data import read_all_data
from services.read_data_by_id import read_data_by_id
from typing import Optional
from datetime import datetime
from config.settings import settings


sensor = APIRouter(prefix='/sensor', tags=['Sensors'])


def validate_sensor_api_key(api_key: str = Header(..., alias="X-API-Key")):
    if not hmac.compare_digest(api_key, settings.SENSOR_API_KEY):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")



@sensor.get('/', response_model=list[SensorDataSchemaRead], status_code=status.HTTP_200_OK)
async def get_all_rows(
    limit: int = Query(10, ge=1, le=100),
    offset: int =0, 
    order: str = Query("desc", pattern="^(asc|desc)$"),
    session: AsyncSession = Depends(get_session),
    start: Optional[datetime] = Query(None, description='Start datetime filter'),
    end: Optional[datetime] = Query(None, description='End datetime filter')
    ):

    
    return await read_all_data(
        limit=limit, 
        offset=offset, 
        session=session, 
        start=start, 
        end=end, 
        order=order)




@sensor.get('/{id}', response_model=SensorDataSchemaRead, status_code=status.HTTP_200_OK)
async def get_data_by_id(id: int, session: AsyncSession = Depends(get_session)):

    try:
        return await read_data_by_id(id, session)
    except ValueError:
        raise HTTPException(status_code=404, detail="Row data not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error")
        




@sensor.post('/', response_model=SensorDataSchemaRead, status_code=status.HTTP_201_CREATED,  dependencies= [Depends(validate_sensor_api_key)])
async def create_row(data: SensorDataSchemaCreate, session: AsyncSession = Depends(get_session) ):

    try:
        return await enter_row(data, session)

    except:
        raise HTTPException(status_code=500, detail="Error inserting sensor data")