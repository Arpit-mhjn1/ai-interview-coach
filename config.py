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
    """Returns the configured LLM instance."""
    provider = os.environ.get("MODEL_PROVIDER", "gemini")
    
    if provider == "gemini":
        google_key = os.environ.get("GOOGLE_API_KEY")
        if not google_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment.")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=google_key)
    elif provider == "openai":
        openai_key = os.environ.get("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY is not set in environment.")
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_key)
    else:
        raise ValueError(f"Unsupported MODEL_PROVIDER: {provider}")
