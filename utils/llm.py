
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

def generate_text(prompt: str) -> dict:
    """
    Generates text using Google Gemini.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    usage = {}
    if response.usage_metadata:
        usage = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count
        }
    return {"text": response.text, "usage": usage}

def generate_structured_json(prompt: str, response_schema: str = None) -> dict:
    """
    Generates a response in JSON format.
    Adds instruction to output strictly valid JSON.
    Returns a dict with 'text' and 'usage'.
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
    usage = {}
    if response.usage_metadata:
        usage = {
            "prompt_token_count": response.usage_metadata.prompt_token_count,
            "candidates_token_count": response.usage_metadata.candidates_token_count,
            "total_token_count": response.usage_metadata.total_token_count
        }
    return {"text": response.text, "usage": usage}
