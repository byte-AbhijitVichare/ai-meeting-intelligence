import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(10)
)
def generate_with_retry(prompt):
    response = model.generate_content(prompt)
    return response.text

def summarize_meeting(transcript):

    transcript = transcript[:8000]

    prompt = f"""
    Analyze this meeting transcript.

    Return:

    1. Executive Summary
    2. Key Discussion Points
    3. Decisions Made
    4. Action Items
    5. Deadlines

    Transcript:
    {transcript}
    """

    try:
        return generate_with_retry(prompt)

    except Exception:
        return """
    ⚠️ Gemini API limit reached.

    Please wait a few minutes and try again.

    This is a temporary free-tier quota limitation.
    """
    
def extract_action_items(transcript):

    transcript = transcript[:8000]

    prompt = f"""
    Extract action items from the transcript.

    Return ONLY valid JSON.

    Format:

    [
      {{
        "person": "",
        "task": "",
        "deadline": ""
      }}
    ]

    Transcript:
    {transcript}
    """

    try:

        text = generate_with_retry(prompt)

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "")

        return json.loads(text)

    except Exception as e:

        print("Action Item Error:", e)

        return []