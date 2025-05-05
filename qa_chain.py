from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from vector_store import VectorStore
from typing import Optional, Dict, Any

class QAChain:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        self.qa_chain = None
        
        # Шаблон для промпта
        self.prompt_template = """Используя следующий контекст, ответьте на вопрос.
        Если вы не знаете ответа, скажите, что не знаете. Не пытайтесь придумать ответ.
        
        Контекст: {context}
        
        Вопрос: {question}
        
        Ответ:"""
        
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
    
    def initialize_chain(self):
        """Инициализирует цепочку вопросов и ответов."""
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.vectorstore.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Задает вопрос и получает ответ."""
        if self.qa_chain is None:
            self.initialize_chain()
        
        try:
            result = self.qa_chain({"query": question})
            return {
                "answer": result["result"],
                "sources": [doc.page_content for doc in result["source_documents"]]
            }
        except Exception as e:
            return {
                "answer": f"Произошла ошибка при обработке вопроса: {str(e)}",
                "sources": []
            } 