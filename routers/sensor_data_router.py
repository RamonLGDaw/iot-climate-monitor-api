# import hmac
# from fastapi import APIRouter, Header, Request, status, Depends, HTTPException, Query
# from schemas.sensor_data_schema import SensorDataSchemaCreate, SensorDataSchemaRead
# from config.db import get_session
# from sqlalchemy.ext.asyncio import  AsyncSession
# from services.create_row import enter_row
# from services.read_data import read_all_data
# from services.read_data_by_id import read_data_by_id
# from typing import Optional
# from datetime import datetime
# from config.settings import settings


# sensor = APIRouter(prefix='/sensor', tags=['Sensors'])


# def validate_sensor_api_key(api_key: str = Header(..., alias="X-API-Key")):
#     if not hmac.compare_digest(api_key, settings.SENSOR_API_KEY):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")



# @sensor.get('/', response_model=list[SensorDataSchemaRead], status_code=status.HTTP_200_OK)
# async def get_all_rows(
#     limit: int = Query(10, ge=1, le=100),
#     offset: int =0, 
#     order: str = Query("desc", pattern="^(asc|desc)$"),
#     session: AsyncSession = Depends(get_session),
#     start: Optional[datetime] = Query(None, description='Start datetime filter'),
#     end: Optional[datetime] = Query(None, description='End datetime filter')
#     ):

    
#     return await read_all_data(
#         limit=limit, 
#         offset=offset, 
#         session=session, 
#         start=start, 
#         end=end, 
#         order=order)




# @sensor.get('/{id}', response_model=SensorDataSchemaRead, status_code=status.HTTP_200_OK)
# async def get_data_by_id(id: int, session: AsyncSession = Depends(get_session)):

#     try:
#         return await read_data_by_id(id, session)
#     except ValueError:
#         raise HTTPException(status_code=404, detail="Row data not found")
#     except Exception:
#         raise HTTPException(status_code=500, detail="Unexpected error")
        




# @sensor.post('/', response_model=SensorDataSchemaRead, status_code=status.HTTP_201_CREATED,  dependencies= [Depends(validate_sensor_api_key)])
# async def create_row(data: SensorDataSchemaCreate, session: AsyncSession = Depends(get_session) ):

#     try:
#         return await enter_row(data, session)

#     except:
#         raise HTTPException(status_code=500, detail="Error inserting sensor data")



# routers/sensor_data_router.py

# routers/sensor_data_router.py
import hmac
from datetime import datetime
from typing import Optional, Literal

from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    Query,
    Security,
)
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_session
from config.settings import settings
from schemas.sensor_data_schema import SensorDataSchemaCreate, SensorDataSchemaRead
from services.create_row import enter_row
from services.read_data import read_all_data
from services.read_data_by_id import read_data_by_id


# --- Router principal ---
sensor = APIRouter(prefix="/sensor", tags=["Sensors"])

# --- Seguridad con API Key ---
api_key_header = APIKeyHeader(
    name="X-API-Key",
    scheme_name="SensorAPIKey",
    auto_error=False, 
)

def validate_sensor_api_key(api_key: Optional[str] = Security(api_key_header)):
    if not api_key or not hmac.compare_digest(api_key, settings.SENSOR_API_KEY):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return True


# --- Endpoints ---
@sensor.get(
    "/",
    response_model=list[SensorDataSchemaRead],
    status_code=status.HTTP_200_OK,
    summary="Listar lecturas",
    description=(
        "Devuelve lecturas paginadas. Admite filtros por rango temporal (`start`, `end`) "
        "y orden por fecha en el servidor vía `order` (`desc` por defecto). "
        "Fechas en **ISO 8601** (UTC), por ejemplo: `2025-08-27T12:00:00Z`."
    ),
    responses={
        200: {"description": "Lista de lecturas"},
        422: {"description": "Parámetros inválidos"},
    },
)
async def get_all_rows(
    limit: int = Query(10, ge=1, le=100, description="Número de registros a devolver"),
    offset: int = Query(0, ge=0, description="Desplazamiento, múltiplo de `limit`"),
    order: Literal["asc", "desc"] = Query(
        "desc", description="Orden por fecha en servidor (ascendente o descendente)"
    ),
    session: AsyncSession = Depends(get_session),
    start: Optional[datetime] = Query(None, description="Fecha/hora inicio (ISO 8601, UTC)"),
    end: Optional[datetime] = Query(None, description="Fecha/hora fin (ISO 8601, UTC)"),
):
    return await read_all_data(
        limit=limit, offset=offset, session=session, start=start, end=end, order=order
    )


@sensor.get(
    "/{id}",
    response_model=SensorDataSchemaRead,
    status_code=status.HTTP_200_OK,
    summary="Obtener lectura por ID",
    description="Devuelve una lectura de sensor según su ID único.",
    responses={
        200: {"description": "Lectura encontrada"},
        404: {"description": "No existe una lectura con ese ID"},
        500: {"description": "Error inesperado"},
    },
)
async def get_data_by_id(id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await read_data_by_id(id, session)
    except ValueError:
        raise HTTPException(status_code=404, detail="Row data not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error")


@sensor.post(
    "/",
    response_model=SensorDataSchemaRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(validate_sensor_api_key)],
    summary="Crear nueva lectura (protegido por API Key)",
    description="Crea una nueva lectura con `temp` y `hum`. Requiere cabecera `X-API-Key` válida.",
    responses={
        201: {"description": "Lectura creada"},
        403: {"description": "API Key inválida o ausente"},
        422: {"description": "Payload inválido"},
        500: {"description": "Error insertando datos"},
    },
)
async def create_row(data: SensorDataSchemaCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await enter_row(data, session)
    except Exception:
        raise HTTPException(status_code=500, detail="Error inserting sensor data")

