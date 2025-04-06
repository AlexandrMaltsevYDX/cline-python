from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    # Настройки из .env файла для подключения к БД
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "db"

    # Прочие настройки
    DB_ECHO: bool = False
    DEBUG: bool = False

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Собирает URL для подключения к базе данных из отдельных компонентов.
        """
        # Используем f-string для форматирования URL
        # psycopg требует postgresql+psycopg://...
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"  # Указывает файл с переменными окружения
        # Добавляем чувствительность к регистру, если переменные в .env могут быть в разном регистре
        # env_case_sensitive = False
        # Для переменных типа DB_PASS можно добавить extra='ignore', если не хотите их утечки при __repr__
        # extra = 'ignore'


# Создаём экземпляр настроек
settings = Settings()
