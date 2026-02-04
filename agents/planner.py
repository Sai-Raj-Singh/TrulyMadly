
import json
from utils.llm import generate_structured_json

SCHEMA = """
{
  "city": "string",
  "activity": "string",
  "date_time_range": "string",
  "intent": "string (brief description of user goal)"
}
"""

def create_plan(user_query: str):
    """
    Analyzes user intent and extracts city, activity, and timeframe.
    """
    prompt = f"""
    You are a Planner Agent for an outdoor activity recommender.
    Your job is to extract the following from the user's query:
    1. City/Location (inferred if not explicit, defaulting to a major nearby city if vague, but prefer explicit)
    2. Activity (e.g., cricket, jogging)
    3. Date/Time Range (e.g., 'tomorrow morning', 'this weekend'). If not specified, assume 'today'.
    
    User Query: "{user_query}"
    
    Output strictly in the following JSON format:
    """
    response_text = None
    try:
        response_text = generate_structured_json(prompt, SCHEMA)
        cleaned_text = response_text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_text)
    except Exception as e:
        return {"error": f"Failed to parse plan: {str(e)}", "raw_response": response_text}
