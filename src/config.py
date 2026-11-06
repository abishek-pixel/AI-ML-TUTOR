"""Configuration management for the AI Tutor."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    
    # Paths
    DATA_DIR = "data"
    MODELS_DIR = "models"
    OUTPUTS_DIR = "outputs"
    NOTES_FILE = os.path.join(DATA_DIR, "sample_notes.txt")
    VECTOR_STORE_PATH = os.path.join(MODELS_DIR, "faiss_index")
    
    # Model Settings
    SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
    DIFFUSION_MODEL = "stabilityai/sd-turbo"
    BLIP_MODEL = "Salesforce/blip-image-captioning-base"
    
    # Generation Settings
    MAX_TOKENS = 1000
    DEFAULT_TEMPERATURE = 0.7
    SIMILARITY_THRESHOLD = 0.6
    
    # UI Settings
    APP_TITLE = "AI-ML-DL Concept Tutor"
    APP_DESCRIPTION = "Learn AI/ML/DL concepts at your level with interactive explanations"
    
    @staticmethod
    def get_api_key():
        """Get the appropriate API key based on provider."""
        if Config.LLM_PROVIDER == "gemini":
            return Config.GEMINI_API_KEY
        elif Config.LLM_PROVIDER == "groq":
            return Config.GROQ_API_KEY
        return ""
    
    @staticmethod
    def validate():
        """Validate configuration."""
        if not Config.get_api_key():
            raise ValueError(f"API key for {Config.LLM_PROVIDER} not found in environment")
        return True
