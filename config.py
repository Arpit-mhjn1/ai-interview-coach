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
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini").lower()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_llm():
    """Returns the configured LLM instance."""
    if MODEL_PROVIDER == "gemini":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in environment.")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
    elif MODEL_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment.")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    else:
        raise ValueError(f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}")
