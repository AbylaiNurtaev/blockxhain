import os
from dotenv import load_dotenv
from typing import Optional

def load_environment_variables():
    """Загружает переменные окружения из .env файла."""
    load_dotenv()
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(
            f"Отсутствуют следующие переменные окружения: {', '.join(missing_vars)}"
        )

def format_sources(sources: list) -> str:
    """Форматирует список источников для отображения."""
    if not sources:
        return "Источники не указаны"
    
    formatted_sources = "\n\nИсточники:\n"
    for i, source in enumerate(sources, 1):
        formatted_sources += f"{i}. {source}\n"
    
    return formatted_sources 