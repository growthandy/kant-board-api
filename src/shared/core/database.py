import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from shared.core.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/board"
)

pool_options = (
    {
        "pool_size": int(os.getenv("CONNECTION_POOL_SIZE", "10")),
        "max_overflow": int(os.getenv("CONNECTION_POOL_MAX_SIZE", "20")),
        "pool_recycle": 1800,
        "pool_pre_ping": True,
    }
    if DATABASE_URL.startswith("postgresql")
    else {}
)

engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    **pool_options,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,  # 비동기에서 commit 후 지연 SELECT → MissingGreenlet 방지
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """요청 하나 = 세션 하나 = 트랜잭션 하나."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def close_db() -> None:
    """서버 종료(lifespan 끝) 때 커넥션 풀을 반납한다."""
    logger.info("데이터베이스 커넥션 풀을 종료합니다.")
    await engine.dispose()
