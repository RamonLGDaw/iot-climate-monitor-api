from fastapi import FastAPI
from routers.sensor_data_router import sensor
from sqlalchemy import text
from config.db import engine

app = FastAPI()

app.include_router(sensor)

@app.get("/health_check")
async def health_check():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "ok", "db": value}