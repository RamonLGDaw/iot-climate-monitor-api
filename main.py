from fastapi import FastAPI
from routers.sensor_data_router import sensor
from sqlalchemy import text
from config.db import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGINS = [
    "http://localhost:5173",                 # dev Vite
    "https://control-clima-front.vercel.app",   # prod front
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,                  # ok si apuntas a orígenes concretos
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)


app.include_router(sensor)

@app.get("/health_check")
async def health_check():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "ok", "db": value}