from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import secrets
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

engine = create_async_engine(
        secrets.DATABASE_URL,
        echo=True
    )

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with session() as s:
        yield s