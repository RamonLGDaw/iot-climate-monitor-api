import asyncio
from sqlalchemy import text
from config.db import engine



async def check_connection():

    try:
        async with engine.connect() as connection:
            result =await connection.execute(text('SELECT 1'))
            print('Connection successful:', result.scalar())

    except Exception as e:
        print("Connection failed: ", e)


asyncio.run(check_connection())