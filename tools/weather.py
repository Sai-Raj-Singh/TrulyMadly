
import os
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
from functools import lru_cache

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

@lru_cache(maxsize=100)
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_weather_forecast(city: str):
    """
    Fetches 5-day weather forecast for a given city.
    Retries 3 times on failure and caches results.
    """
    if not API_KEY:
        return {"error": "OPENWEATHER_API_KEY not found"}

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Weather API Error: {e}") 
        # Reraise for retry mechanism to work on transient errors, 
        # but for fatal errors (404, 401) we might want to stop.
        # Simple retry here catches all RequestExceptions.
        raise e 

