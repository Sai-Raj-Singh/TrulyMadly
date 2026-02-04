
import os
import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed
from functools import lru_cache

load_dotenv()

API_KEY = os.getenv("WAQI_API_KEY")
BASE_URL = "https://api.waqi.info/feed"

@lru_cache(maxsize=100)
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_air_quality(city: str):
    """
    Fetches real-time air quality index (AQI) for a city.
    Retries 3 times on failure and caches results.
    """
    if not API_KEY:
        return {"error": "WAQI_API_KEY not found"}

    url = f"{BASE_URL}/{city}/"
    params = {
        "token": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"AQI API Error: {e}")
        raise e
