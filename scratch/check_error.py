import os
from google import genai
from google.genai import errors
from dotenv import load_dotenv

def check_error_type():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    try:
        # Intentionally use the busy model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="test"
        )
        print("Success")
    except Exception as e:
        print(f"Type of error: {type(e)}")
        print(f"Error string: {str(e)}")
        # Check if it's a specific SDK error
        # if isinstance(e, errors.BaseError): ...

if __name__ == "__main__":
    check_error_type()
