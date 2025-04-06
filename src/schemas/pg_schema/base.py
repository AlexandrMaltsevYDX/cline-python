from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.settings import settings

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]



class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
