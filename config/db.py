from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings



engine = create_async_engine(settings.DATABASE_URL, echo=True)
#! Falta configurar el pool y sacar el echo=True antes de producción

asyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_session() -> AsyncSession: #  type: ignore
    async with asyncSessionLocal() as session:
        yield session




