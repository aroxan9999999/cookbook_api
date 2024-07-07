from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://aroxan:********@localhost/cookbook_"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
