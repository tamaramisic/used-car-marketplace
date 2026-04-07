from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import db_settings

engine = create_async_engine(
    db_settings.POSTGRES_URL,
    echo=True,
)

async def get_session():
    async_session = async_sessionmaker(
        bind=engine, 
        expire_on_commit=False, 
        class_=AsyncSession
    )

    async with async_session() as session:
        yield session
