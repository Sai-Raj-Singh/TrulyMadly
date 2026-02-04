
import json
from utils.llm import generate_text

def verify_and_recommend(execution_result: dict):
    """
    Analyzes API data and generates a final recommendation report.
    """
    if "error" in execution_result:
        return f"Error during execution: {execution_result['error']}"

    plan = execution_result.get("plan", {})
    weather = execution_result.get("weather_data", {})
    aqi = execution_result.get("aqi_data", {})
    
    # Check for missing data
    missing_info = []
    if "error" in weather or not weather:
        missing_info.append("Weather data unavailable")
    if "error" in aqi or not aqi:
        missing_info.append("Air Quality data unavailable")

    fallback_note = ""
    if missing_info:
        fallback_note = f"\nWARNING: Some data is missing ({', '.join(missing_info)}). Provide a cautious recommendation based on general knowledge for the location/season if possible, but strictly warn the user about missing real-time data."

    prompt = f"""
    You are a Verifier Agent and Outdoor Activity Expert.
    
    User Request: "{plan.get('intent', 'N/A')}"
    Target Activity: {plan.get('activity', 'N/A')}
    Target Date/Time: {plan.get('date_time_range', 'N/A')}
    Target City: {plan.get('city', 'N/A')}

    Real-time Environment Data:
    
    1. Air Quality Data (WAQI):
    {json.dumps(aqi, indent=2)}

    2. Weather Forecast Data (OpenWeatherMap):
    {json.dumps(weather, indent=2)}

    {fallback_note}

    Your Mission:
    1. Analyze the weather (rain, temp, wind) and air quality (AQI) for the requested time.
    2. Check for unsafe conditions (e.g., high AQI > 100 might be bad for jogging, rain is bad for tennis).
    3. Provide a clear, human-readable recommendation. 
       - Start with a verdict: "YES", "MAYBE", or "NO".
       - Explain WHY using the data (cite temp, rain status, AQI level).
       - If unsafe, suggest an alternative time if obvious from the forecast data.
       - If data is missing, perform a best-effort check but prioritize safety.
    """

    response = generate_text(prompt)
    return response
