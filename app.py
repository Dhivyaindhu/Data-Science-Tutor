# -*- coding: utf-8 -*-
"""Untitled146.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qshuc9OKryXoGJnuJwtU7Ai7WC096C0c
"""

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage
import os
st.title("Data Science Tutor")
gemini_API_KEY = "AIzaSyDfZ11gOPEbZ0LDEgMGe7DG__XS5Su7uYo"   
chat_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI assistant specializing in Data Science. Your role is to help users solve problems, understand concepts, theories, and methods. "
     "You have expertise in tools like Power BI, Tableau, and Excel and also related fields like Machine Learning and Artificial Intelligence. "
     "Additionally, you provide guidance on Data Science projects and interview preparation. "
     "You also act as a code reviewer, offering constructive feedback on code quality, optimization, and best practices. "
     "If a user asks a question that is unrelated to Data Science or AI, respond with: "
     "'I specialize in Data Science and AI. Unfortunately, I cannot answer that question.'"),

    ("human",
     "Provide a structured question set that progresses from basic to advanced levels in the field of Data Science.")
])

chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_API_KEY)
parser = StrOutputParser()
Queries=st.text_input("Enter your question")
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()
image_input = st.file_uploader("Upload an image (photo ad)", type=["jpg", "png", "jpeg"])
doc_input = st.file_uploader("Upload a document (PDF)", type=["pdf"])
# Process Input
if st.button("Generate Response"):
    messages = []

    # Add text input
    if Queries:
        messages.append(HumanMessage(content=Queries))

    # Process image input
    if image_input:
        encoded_image = encode_image(image_input)
        messages.append(HumanMessage(content={"image": encoded_image}))

    # Process document input
    if doc_input:
        document_text = extract_text_from_pdf(doc_input)
        messages.append(HumanMessage(content=document_text))
    if messages:
        response = chat_model.invoke(messages)
        main_content = response.content  # Extracts the main text content
        st.write(main_content)
        parsed_response = parser.parse(response.content)  # Parse only the main content
        st.write(parsed_response)
        response = chat_model.invoke(messages)
        main_content = response.content
        st.write(main_content)



    else:
        st.warning("Please enter a query, upload an image, or provide a document.")



        
