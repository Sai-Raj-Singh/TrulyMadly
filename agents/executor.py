
import concurrent.futures
from tools.weather import get_weather_forecast
from tools.air_quality import get_air_quality

def execute_plan(plan: dict):
    """
    Fetches real data based on the plan.
    Uses ThreadPoolExecutor to fetch Weather and AQI data in parallel.
    """
    if "error" in plan:
        return {"error": "Plan execution aborted due to planning error", "details": plan}

    city = plan.get("city")
    if not city:
        return {"error": "City not found in plan"}

    weather_data = {}
    aqi_data = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_weather = executor.submit(get_weather_forecast, city)
        future_aqi = executor.submit(get_air_quality, city)

        try:
            weather_data = future_weather.result()
        except Exception as e:
            weather_data = {"error": f"Weather fetch failed: {str(e)}"}

        try:
            aqi_data = future_aqi.result()
        except Exception as e:
            aqi_data = {"error": f"AQI fetch failed: {str(e)}"}

    return {
        "plan": plan,
        "weather_data": weather_data,
        "aqi_data": aqi_data
    }
