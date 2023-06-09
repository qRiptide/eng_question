from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db_conf import settings

engine = create_async_engine(settings.asyncpg_url, echo=True)
AsyncSessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
