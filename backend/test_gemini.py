import os
from dotenv import load_dotenv
from google.genai import Client

# Load environment variables
load_dotenv()

keys = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

print("=== Gemini API Key Batch Test ===\n")

for i, api_key in enumerate(keys, 1):
    if not api_key:
        print(f"KEY {i}: MISSING in .env")
        continue

    print(f"KEY {i} (starting with {api_key[:10]}...):")
    try:
        client = Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say 'Key valid'",
        )
        print(f"  RESULT: SUCCESS! ({response.text.strip()})")
    except Exception as e:
        print("  RESULT: FAILED!")
        print(f"  ERROR: {str(e)[:100]}...")
    print("-" * 30)

