import streamlit as st
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import base64
import PyPDF2
import io
import os

st.title("Data Science Tutor")

gemini_API_KEY = os.getenv("GEMINI_API_KEY")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_API_KEY)

def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

Queries = st.text_input("Enter your question")
doc_input = st.file_uploader("Upload a document (PDF)", type=["pdf"])

if st.button("Generate Response"):
    messages = []

    if Queries:
        messages.append(HumanMessage(content=Queries))

    if doc_input:
        document_text = extract_text_from_pdf(doc_input)
        messages.append(HumanMessage(content=document_text))

    if messages:
        response = chat_model.invoke(messages)
        st.write(response.content)
    else:
        st.warning("Please enter a query or upload a document.")
