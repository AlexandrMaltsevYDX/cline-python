from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from .settings import settings

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]


engine = create_async_engine(
            settings.DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True,
            echo=settings.DB_ECHO,
        )

session_factory = async_sessionmaker(
            engine, 
            class_=AsyncSession, 
            expire_on_commit=False, 
            autocommit=False, 
            autoflush=False,
        )


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> "AbstractUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
    
    
class PGUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory
        self.session: AsyncSession = None

    async def __aenter__(self) -> "PGUnitOfWork":
        self.session = await self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
