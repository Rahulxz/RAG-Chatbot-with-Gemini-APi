import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class ChatGemini:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file.")
        genai.configure(api_key=api_key)
        
        # ⚠️ Fix is here: Updated to the current, supported model name.
        self.model = genai.GenerativeModel("gemini-2.5-flash") 

    def get_response(self, prompt):
        try:
            # The generate_content method is correct for the Python SDK
            response = self.model.generate_content(prompt) 
            return response.text
        except Exception as e:
            # It's better to catch the specific API error for better debugging, 
            # but this general catch is fine for now.
            return f"⚠️ Gemini API Error: {e}"