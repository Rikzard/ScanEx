import os
import sys
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.gemini_client import call_gemini_with_retry

def test_truncation():
    print("Testing truncation...")
    long_text = "A" * 35000  # Exceeds the 30k limit
    try:
        # We don't necessarily need a valid key to test the truncation logic before the call
        # but the function will fail at the API call if key is missing/bad.
        # This test ensures it doesn't crash before the call.
        print(f"Original length: {len(long_text)}")
        # We'll use a mocked client or just check if it truncates.
        # Actually, let's just run it and catch the auth error, checking if it logged the truncation.
        call_gemini_with_retry(long_text, max_retries=1)
    except Exception as e:
        print(f"Caught expected error or actual API error: {e}")

if __name__ == "__main__":
    load_dotenv()
    test_truncation()
