import os
import google.generativeai as genai


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key = GOOGLE_API_KEY)

def generate_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text