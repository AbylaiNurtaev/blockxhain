from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["constitution_assistant"]
        self.qa_collection = self.db["qa_history"]
    
    def save_qa(self, question: str, answer: str, sources: List[str]) -> str:
        """Сохраняет вопрос и ответ в базу данных."""
        qa_doc = {
            "question": question,
            "answer": answer,
            "sources": sources,
            "timestamp": datetime.utcnow()
        }
        result = self.qa_collection.insert_one(qa_doc)
        return str(result.inserted_id)
    
    def get_qa_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получает историю вопросов и ответов."""
        history = self.qa_collection.find().sort("timestamp", -1).limit(limit)
        return [
            {
                "question": doc["question"],
                "answer": doc["answer"],
                "sources": doc["sources"],
                "timestamp": doc["timestamp"]
            }
            for doc in history
        ]
    
    def close(self):
        """Закрывает соединение с базой данных."""
        self.client.close() 