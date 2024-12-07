from typing import AsyncGenerator

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession #异步会话
from sqlalchemy.ext.asyncio import create_async_engine #创建异步引擎
from sqlalchemy.orm import sessionmaker #会话工厂
from app.core.config import settings

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # 设置为 True 可以打印 SQL 语句，生产环境建议设为 False
    future=True
)

# 创建异步会话工厂
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """初始化数据库，创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话的依赖函数
    用法：
    @app.get("/items/")
    async def get_items(db: AsyncSession = Depends(get_db)):
        ...
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()