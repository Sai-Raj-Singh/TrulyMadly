
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash" 

def generate_text(prompt: str) -> str:
    """
    Generates text using Google Gemini.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    if response.usage_metadata:
        print(f"Token Usage (Text): {response.usage_metadata}")
    return response.text

def generate_structured_json(prompt: str, response_schema: str = None) -> str:
    """
    Generates a response in JSON format.
    Adds instruction to output strictly valid JSON.
    """
    
    config = types.GenerateContentConfig(
        response_mime_type="application/json"
    )

    full_prompt = f"{prompt}"
    if response_schema:
        full_prompt += f"\n\nPlease output strictly in the following JSON schema:\n{response_schema}"

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
        config=config
    )
    if response.usage_metadata:
        print(f"Token Usage (JSON): {response.usage_metadata}")
    return response.text
