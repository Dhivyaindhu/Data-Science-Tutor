# -*- coding: utf-8 -*-
import streamlit as st
import base64
import io
import PyPDF2
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

st.title("Data Science Tutor")

# Secure API Key Handling (Replace with env variable for security)
gemini_API_KEY = "AIzaSyDfZ11gOPEbZ0LDEgMGe7DG__XS5Su7uYo"

# Define the chat template
chat_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI assistant specializing in Data Science. Your role is to help users solve problems, understand concepts, theories, and methods. "
     "You have expertise in tools like Power BI, Tableau, and Excel and also related fields like Machine Learning and Artificial Intelligence. "
     "Additionally, you provide guidance on Data Science projects and interview preparation. "
     "You also act as a code reviewer, offering constructive feedback on code quality, optimization, and best practices. "
     "If a user asks a question that is unrelated to Data Science or AI, respond with: "
     "'I specialize in Data Science and AI. Unfortunately, I cannot answer that question.'"),

    ("human", "{user_input}")  # Placeholder for dynamic input
])

# Initialize the chat model
chat_model = ChatGoogleGenerativeAI(model="gemini-2.0", google_api_key=gemini_API_KEY)
parser = StrOutputParser()

# Text input
Queries = st.text_input("Enter your question:")

# Function to encode an image
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    return text.strip()

# File uploaders
image_input = st.file_uploader("Upload an image (photo ad)", type=["jpg", "png", "jpeg"])
doc_input = st.file_uploader("Upload a document (PDF)", type=["pdf"])

# Process Input and Generate Response
if st.button("Generate Response"):
    messages = ""

    # Process text input
    if Queries:
        messages += f"User Query: {Queries}\n\n"

    # Process image input
    if image_input:
        encoded_image = encode_image(image_input)
        messages += "Attached Image (Base64 Encoded).\n\n"

    # Process document input
    if doc_input:
        document_text = extract_text_from_pdf(doc_input)
        messages += f"Extracted Document Text:\n{document_text}\n\n"

    # Ensure there's input before calling the model
    if messages:
        final_prompt = chat_template.format(user_input=messages)  # Format the prompt
        response = chat_model.invoke(final_prompt)  # Generate response
        parsed_response = parser.parse(response)  # Parse response
        st.write(parsed_response)  # Display response
    else:
        st.warning("Please enter a question or upload a file before generating a response.")
