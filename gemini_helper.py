import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_safety_alert(count, threshold):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    The current crowd count is {count}, which exceeds the limit of {threshold}.
    Generate a short, urgent safety alert in both Marathi and English.
    Keep it actionable (e.g., 'Please stop entry').
    """
    
    response = model.generate_content(prompt)
    return response.text