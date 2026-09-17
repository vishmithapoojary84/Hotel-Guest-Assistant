import os
from dotenv import load_dotenv
from google import genai
from app.data.loader import load_hotel_data

load_dotenv()

# Initialize Gemini Client
try:
    client = genai.Client()
except Exception as e:
    client = None
    print(f"Warning: Could not initialize GenAI client. Error: {e}")

HOTEL_DATA = load_hotel_data()
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
