from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import db_settings

engine = create_async_engine(
    db_settings.POSTGRES_URL,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
