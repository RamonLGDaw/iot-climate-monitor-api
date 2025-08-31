# from fastapi import FastAPI
# from routers.sensor_data_router import sensor
# from sqlalchemy import text
# from config.db import engine
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# ALLOWED_ORIGINS = [
#     "https://io-t-climate-monitor-front.vercel.app",
#     "*" 

# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=False,        
#     allow_methods=["GET", "POST", "OPTIONS"],
#     allow_headers=["Content-Type", "X-API-Key"],
# )


# app.include_router(sensor)

# @app.get("/health_check")
# async def health_check():
#     async with engine.begin() as conn:
#         result = await conn.execute(text("SELECT 1"))
#         value = result.scalar()
#         return {"status": "ok", "db": value}


# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from config.db import engine
from routers.sensor_data_router import sensor

tags_metadata = [
    {
        "name": "Sensors",
        "description": "Operaciones para **lecturas** de temperatura y humedad. "
                       "Incluye paginación, filtros por fecha y creación de registros (protegido).",
    }
]

app = FastAPI(
    title="IoT Climate Monitor API",
    description=(
        "API asíncrona con FastAPI + SQLAlchemy para almacenar y consultar lecturas "
        "de temperatura y humedad desde Raspberry Pi Pico W.\n\n"
        "Endpoints públicos para lectura y endpoint protegido por API Key para inserción."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Ramon Lage",
        "url": "https://ramonlage-portafolio.vercel.app/",
        "email": "ramonlagegibert@gmail.com",
    },
    license_info={"name": "MIT"},
    docs_url="/docs",
    redoc_url="/redoc",
)

ALLOWED_ORIGINS = ["https://io-t-climate-monitor-front.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)

app.include_router(sensor)

@app.get("/health_check", tags=["Infra"], summary="Comprobar salud de la API y la DB")
async def health_check():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "ok", "db": value}
