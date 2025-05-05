import streamlit as st
from constitution_loader import ConstitutionLoader
from vector_store import VectorStore
from qa_chain import QAChain
from utils import load_environment_variables, format_sources
import os

# Загрузка переменных окружения
load_environment_variables()

# Инициализация компонентов
vector_store = VectorStore()
constitution_loader = ConstitutionLoader()
qa_chain = QAChain(vector_store)

def main():
    st.title("AI Assistant for Kazakhstan Constitution")
    
    # Загрузка файлов
    uploaded_files = st.file_uploader(
        "Загрузите файлы с текстом конституции",
        accept_multiple_files=True,
        type=['txt']
    )
    
    if uploaded_files:
        # Обработка загруженных файлов
        all_texts = []
        for file in uploaded_files:
            text = file.read().decode('utf-8')
            chunks = constitution_loader.load_from_text(text)
            all_texts.extend(chunks)
        
        # Сохранение в векторное хранилище
        vector_store.store_documents(all_texts)
        st.success("Документы успешно загружены и обработаны!")
    
    # Поле для вопросов
    query = st.text_input("Задайте вопрос о конституции:")
    
    if query:
        # Получение ответа
        result = qa_chain.ask_question(query)
        
        # Отображение ответа
        st.write("Ответ:", result["answer"])
        
        # Отображение источников
        st.write(format_sources(result["sources"]))

if __name__ == "__main__":
    main() 