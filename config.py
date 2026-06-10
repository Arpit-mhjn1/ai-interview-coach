import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Settings
APP_TITLE = "AI Interview Coach"
PAGE_ICON = "👔"

# Supported roles
DEFAULT_ROLES = [
    "Software Engineer",
    "Data Scientist",
    "Product Manager",
    "UX Designer",
    "Marketing Specialist",
    "Sales Representative",
    "Custom..."
]

# Model Configuration
def get_llm():
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("GROQ_API_KEY is not set. Please add it to Streamlit Secrets.")
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model="llama-3.3-70b-versatile", 
        temperature=0.7, 
        api_key=groq_key,
        base_url="https://api.groq.com/openai/v1"
    )
