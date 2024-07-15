import base64
import io
from dotenv import load_dotenv
import os
import streamlit as st
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("Google_api_key"))

def get_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def pdf_to_image(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set Streamlit page configuration
st.set_page_config(page_title="Resume Parsing Expert")

st.header("Resume Insight Analyzer")

# Input fields
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

# Buttons
st.subheader("Get insights from the resume")

opt1 = st.button("Tell me about the Resume")
opt2 = st.button("How can I improve my Skills")
opt3 = st.button("Percentage Match")

# Prompts
prompt1 = "You are an experienced HR.You have to review resume. The students might be from engineering background. They may know finance, web development,data analytics and so on. Your task is to review the provided resume against the job description for these profiles. Please share your professional evaluation whether the candidate profile aligns with the job description."
prompt2 = "You are an experienced HR.You have to review resume of college. Your task is to review the resume against the job description and give feedback on how the candidate can improve their skills and what areas they could work on so that they would be fit for the job profile."
prompt3 = "You are a skilled Application Tracking System with deep knowledge in the fields of Data Science, Web development, analytics, engineering, and finance. Your task is to match the provided resume against the job description and give a matching percentage in numbers first. Also, provide list of skills that are missing from the resume but required in job description."

# Handle button clicks
if opt1:
    if uploaded_file is not None:
        pdf_content = pdf_to_image(uploaded_file)
        response = get_response(prompt1, pdf_content,input_text )
        st.subheader("Here is the description of the resume")
        st.write(response)
    else:
        st.write("Upload a resume")

elif opt2:
    if uploaded_file is not None:
        pdf_content = pdf_to_image(uploaded_file)
        response = get_response(prompt2, pdf_content, input_text)
        st.subheader("Here are ways to improve your skills and areas you can work on")
        st.write(response)
    else:
        st.write("Upload a resume")

elif opt3:
    if uploaded_file is not None:
        pdf_content = pdf_to_image(uploaded_file)
        response = get_response(prompt3, pdf_content, input_text)
        st.subheader("Here is the matching percentage of the resume")
        st.write(response)
    else:
        st.write("Upload a resume")
