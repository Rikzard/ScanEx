import os
from google import genai
from dotenv import load_dotenv

def list_models():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print("Listing available models:")
    try:
        # Use the models.list() method if available in this SDK version
        # Some versions use a different approach.
        for model in client.models.list():
            print(f"Name: {model.name}, Display Name: {model.display_name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
