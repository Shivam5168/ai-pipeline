import os
import sys
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable is missing.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

def inspect_code_and_data():
    file_path = "data.json"
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)

    with open(file_path, "r") as f:
        content = f.read()

    prompt = f"""
    You are an automated CI/CD AI Inspector.
    Examine this JSON file content before deployment:
    1. Check for exposed secrets, passwords, or API keys.
    2. Validate that the JSON structure is clean and valid.

    File Content:
    {content}

    Rules:
    - If valid and secure, output ONLY: STATUS: PASS
    - If invalid or contains sensitive data, output ONLY: STATUS: FAIL - [reason]
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        result = response.text.strip()
        print(f"AI Inspector Result: {result}")

        if "STATUS: FAIL" in result:
            print("Validation failed: Deployment blocked by AI Agent.")
            sys.exit(1)
        elif "STATUS: PASS" in result:
            print("Validation passed: Proceeding to deployment.")
            sys.exit(0)
        else:
            print(f"Unexpected AI output: {result}")
            sys.exit(1)

    except Exception as e:
        print(f"API Request failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    inspect_code_and_data()
