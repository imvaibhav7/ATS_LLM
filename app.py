from dotenv import load_dotenv # type: ignore

load_dotenv()
import streamlit as st # type: ignore
import os
import io
import base64
from PIL import Image
import pdf2image # type: ignore
import google.generativeai as genai # type: ignore

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the pdf into image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type": "image/jpeg",
                "data":base64.b64encode(img_byte_arr).decode()   #Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")

# STREAMLIT APP
st.set_page_config(page_title="ATS RESUME EXPERT")
# st.header("ATS")
input_text=st.text_area("Job Description", key="input")
uploaded_file=st.file_uploader("Upload your resume in pdf format",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1=st.button("Tell me about the resume")

submit2=st.button("How can i improvise my skills")

# submit3=st.button("What are the keyword that are missing")

submit3= st.button("Percentage match")

input_prompt_1="""
You are an experienced HR with Tech experience in the field of any one job role from data science, full stack web development, big data engineering, devops,
data analyst, your task is to review the provided resume against the job description for these profiles.
please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strength and weaknesses of the applicant in relation to the specified job requirements.
"""
 
input_prompt_2="""
You are an technical human resource manager with expertise in data science, full stack web development, big data engineering, devops,
data analyst, your role is to scrutinize the resume in the light of job description provided.
Share your insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skill and identify areas of improvement.
"""

input_prompt_3="""
you are an skilled ATS (Applicant tracking system) scanner with a deep understaning of any one job role among data science, full stack web development, big data engineering, devops,
data analyst and deep ATS functionality,
your task is to evaluate the resume against the provided job description. Give me the percentage of match if resume matches
job description. First the output should come as perrcentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt_1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt_3,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt_2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
