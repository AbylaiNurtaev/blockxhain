import streamlit as st
from constitution_loader import ConstitutionLoader
from vector_store import VectorStore
from qa_chain import QAChain
from database import Database
from utils import load_environment_variables, format_sources
import os

# Загрузка переменных окружения
load_environment_variables()

# Инициализация компонентов
vector_store = VectorStore()
constitution_loader = ConstitutionLoader()
qa_chain = QAChain(vector_store)
db = Database()

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
            chunks = constitution_loader.split_text(text)
            all_texts.extend(chunks)
        
        if all_texts:
            vector_store.store_documents(all_texts)
            st.success("Текст успешно обработан!")
    
    # Поле для ввода вопроса
    question = st.text_input("Задайте вопрос о конституции:")
    
    if question:
        # Получение ответа
        result = qa_chain.ask_question(question)
        
        # Сохранение в базу данных
        db.save_qa(question, result["answer"], result["sources"])
        
        # Отображение ответа
        st.write("Ответ:", result["answer"])
        st.write(format_sources(result["sources"]))
    
    # Отображение истории
    st.subheader("История вопросов")
    history = db.get_qa_history()
    for qa in history:
        with st.expander(f"Вопрос: {qa['question']}"):
            st.write("Ответ:", qa["answer"])
            st.write(format_sources(qa["sources"]))
            st.write("Время:", qa["timestamp"].strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main() 