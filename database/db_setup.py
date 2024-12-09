from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import config
from database.models import Base


engine = create_async_engine(config.DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """For local development purposes only"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
