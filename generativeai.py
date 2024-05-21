import os
import streamlit as st
import google.generativeai as genai

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.write("GOOGLE_API_KEY not found")

genai.configure(api_key = GOOGLE_API_KEY)

def generate_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    #model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text