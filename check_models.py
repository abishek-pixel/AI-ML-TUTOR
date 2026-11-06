"""Check available models for the API key."""
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("Checking available Gemini models...")
print("="*60)

try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    print("\nListing available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nThis usually means:")
    print("1. The API key is invalid or expired")
    print("2. There's a network issue")
    print("3. The API endpoint has changed")
    print("\n💡 Solution:")
    print("1. Go to: https://ai.google.dev")
    print("2. Get a NEW API key")
    print("3. Replace it in the .env file")
    print("4. Make sure there are NO extra spaces")
