import os
from google import genai
from dotenv import load_dotenv

def test_model():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Try gemini-2.5-flash since it was in the original code
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="test"
        )
        print(f"Success with gemini-2.5-flash: {response.text}")
    except Exception as e:
        print(f"Error with gemini-2.5-flash: {e}")

if __name__ == "__main__":
    test_model()
