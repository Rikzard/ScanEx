import os
import sys
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.gemini_client import call_gemini_with_retry

def test_retry_on_503():
    load_dotenv()
    print("Testing retry on 503...")
    try:
        # Use gemini-2.5-flash which we know gives 503
        response = call_gemini_with_retry("Hello", model_name='gemini-2.5-flash', max_retries=3)
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed after retries: {e}")

if __name__ == "__main__":
    test_retry_on_503()
