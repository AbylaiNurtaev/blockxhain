from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Optional
import os

class ConstitutionLoader:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_from_file(self, file_path: str) -> List[str]:
        """Загружает текст конституции из файла и разбивает его на чанки."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return self._split_text(text)
        except Exception as e:
            raise Exception(f"Ошибка при загрузке файла: {str(e)}")
    
    def load_from_text(self, text: str) -> List[str]:
        """Разбивает предоставленный текст на чанки."""
        return self._split_text(text)
    
    def _split_text(self, text: str) -> List[str]:
        """Внутренний метод для разбиения текста на чанки."""
        return self.text_splitter.split_text(text) 