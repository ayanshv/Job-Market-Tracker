import pdfplumber
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_pdf_text(pdf_file):
    reader = pdfplumber.open(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text+=extracted


    return text.strip()

def analyze_resume(resume_text, top_skills):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are a career advisor analyzing a resume against current job market data.

      The most in-demand skills in the job market right now are:
      {top_skills}

      Here is the candidate's resume:
      {resume_text}
    
    Please provide the following:
    1. Key strengths you notice in this resume
    2. Skills from the job market list that are missing
    3. Specific recommendations to improve their chances
    4. What types of roles they are best suited for right now
    
    Keep the response concise and actionable
    
    """

    response = model.generate_content(prompt)

    return response.text