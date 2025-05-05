from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.openai import OpenAIEmbeddings
from typing import List
import os

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_store"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
    
    def store_documents(self, documents: List[str], metadata: List[dict] = None):
        """Сохраняет документы в векторное хранилище."""
        if metadata is None:
            metadata = [{} for _ in documents]
        
        self.vectorstore = Chroma.from_texts(
            texts=documents,
            embedding=self.embeddings,
            metadatas=metadata,
            persist_directory=self.persist_directory
        )
        self.vectorstore.persist()
    
    def load_store(self):
        """Загружает существующее векторное хранилище."""
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
    
    def similarity_search(self, query: str, k: int = 4):
        """Выполняет поиск похожих документов."""
        if self.vectorstore is None:
            raise Exception("Векторное хранилище не инициализировано")
        return self.vectorstore.similarity_search(query, k=k)
    
    def clear_store(self):
        """Очищает векторное хранилище."""
        if os.path.exists(self.persist_directory):
            import shutil
            shutil.rmtree(self.persist_directory) 