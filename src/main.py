from fastapi import FastAPI
import uvicorn

# Импортируем роутер из вашего юзкейса
import use_cases.blacklist_management.router as blacklist_management_router
# Импортируем настройки, если они нужны глобально (например, для заголовка)
# from app.settings import settings

# Можно добавить lifespan для инициализации/очистки ресурсов, если нужно
# from contextlib import asynccontextmanager
# from typing import AsyncIterator
# from app.db import engine # Пример

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncIterator[None]:
#     # Код инициализации при старте (например, проверка соединения с БД)
#     print("Starting up...")
#     yield
#     # Код очистки при остановке (например, закрытие соединений)
#     print("Shutting down...")
#     # await engine.dispose() # Пример

# Создаем экземпляр FastAPI
# app = FastAPI(lifespan=lifespan, title="My Blacklist API") # Пример с lifespan
app = FastAPI(title="Blacklist Management API")

# Добавляем простой корневой эндпоинт
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Blacklist Management API"}

# Подключаем роутер для управления черным списком
app.include_router(blacklist_router_module.router)

# Блок для запуска через `uvicorn src.main:app --reload` (необязательно, если запускаете иначе)
if __name__ == "__main__":
    # Используйте настройки из settings, если они определяют host/port
    # uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
    # Или просто для примера:
    uvicorn.run(app, host="127.0.0.1", port=8000)
