import os
import sys
from google import genai

# Initialize the Gemini API client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def inspect_code_and_data():
    # Read files to be pushed to S3
    with open("data.json", "r") as f:
        content = f.read()

    prompt = f"""
    You are an automated CI/CD AI Agent.
    Inspect the following file content before deployment to S3:
    1. Check for any hardcoded API keys, secrets, or sensitive tokens.
    2. Check if the JSON is valid and structurally sound.
    
    Content:
    {content}
    
    If safe and valid, respond ONLY with "STATUS: PASS".
    If issues exist, respond with "STATUS: FAIL - [reason]".
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    result = response.text.strip()
    print(f"AI Inspector Output: {result}")

    if "STATUS: FAIL" in result:
        print("Build blocked by Gemini CI Agent.")
        sys.exit(1)

if __name__ == "__main__":
    inspect_code_and_data()