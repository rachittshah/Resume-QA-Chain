\import streamlit as st
import pdfplumber
from docx import Document
import openai
import tempfile
import os
import base64
from pdf2jpg import pdf2jpg
import numpy as np
from PIL import Image
import time
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)

 # Access the API key from Streamlit secrets
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to parse PDF files
def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text += page.extract_text()
    return text

# Function to parse DOCX files
def parse_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to analyze text with OpenAI API
def analyze_with_openai(text):
    model = "gpt-3.5-turbo-16k"
    messages = [
    {
        "role": "system",
        "content": "You are an advanced document analyzer. Your task is to determine if the provided text is a resume or not. If it's a resume, return only resume."
    },
    {
        "role": "user",
        "content": text
    }]

    response = openai.ChatCompletion.create(model=model, messages=messages)
    print(response)
    if 'resume' in response['choices'][0]['message']['content'].lower():
        messages.append({
            "role": "system",
            "content": "You are an advanced resume reviewer specialized in identifying and evaluating both technical and interpersonal skills. Your expertise enables you to formulate incisive questions that hiring managers can use to gain a deeper understanding of a candidate's qualifications and character."
        })
        messages.append({
            "role": "user",
            "content": f"Based on the resume information provided, please structure the key points in bullet format and formulate a set of 10 questions designed to evaluate the candidate's technical skills, interpersonal abilities, and overall fit for a prospective role. Here is the resume content: {text}"
        })
        response = openai.ChatCompletion.create(model=model, messages=messages)
        return response['choices'][0]['message']['content']
    else:
        return "The uploaded document does not appear to be a resume. Please upload a resume."

# Function to render PDF
def write_pdf(pdf_path, display_method="images"):
    if display_method == "images":
        tmp_sub_folder_path = tempfile.mkdtemp()
        result = pdf2jpg.convert_pdf2jpg(pdf_path, tmp_sub_folder_path, pages="ALL")
    print("Type of result:", type(result))
    print("Value of result:", result)
    if isinstance(result, bool):
        st.error("Failed to convert PDF to JPG. Please check the PDF file.")
        return
        images = []
        for image_path in result[0]["output_jpgfiles"]:
            images.append(np.array(Image.open(image_path)))
        merged_arr = np.concatenate(images)
        merged_path = os.path.join(tmp_sub_folder_path, "merged.jpeg")
        Image.fromarray(merged_arr).save(merged_path)
        st.image(merged_path)
    else:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f"""
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}" 
                width="275%" height="800px" type="application/pdf"
            >
            </iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)

# Custom CSS to make the webpage width wider
def custom_css():
    st.markdown("""
        <style>
            .reportview-container {
                max-width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

custom_css()

# Main Streamlit app
st.title("Resume Analyzer")

# Progress Bar and Status Text
progress_bar = st.progress(0)
status_text = st.empty()

# File Uploader
uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"], key="unique_key")

if uploaded_file:
    st.success("File successfully uploaded.")
    status_text.text("Parsing your file...")
    progress_bar.progress(20)

    if uploaded_file.type == "application/pdf":
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tfile.write(uploaded_file.read())
        extracted_text = parse_pdf(tfile.name)
        
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        tfile.write(uploaded_file.read())
        extracted_text = parse_docx(tfile.name)

    status_text.text("Analyzing with OpenAI...")
    progress_bar.progress(50)
    
    result = analyze_with_openai(extracted_text)

    status_text.text("Analysis complete.")
    progress_bar.progress(100)

    col1, col2 = st.columns([1,2])  # This creates two columns with col2 twice as wide as col1
        
    col1, col2 = st.columns([2,1])  # This creates two columns with col1 twice as wide as col2
    
    with col1:
        st.header("Resume Analysis")
        st.write(result)
            
        # Download analysis result
        b64 = base64.b64encode(result.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="analysis.txt">Download Analysis</a>'
        st.markdown(href, unsafe_allow_html=True)
            
    with col2:
        st.header("Your Resume")
        if uploaded_file.type == "application/pdf":
            write_pdf(tfile.name)
        else:
            st.write(extracted_text)


