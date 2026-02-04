
import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Outdoor Activity Planner", layout="wide")

st.title("AI Outdoor Activity & Sports Planner")
st.markdown("Get AI-powered recommendations based on real-time weather and air quality.")

API_URL = "http://127.0.0.1:8000/query"

query = st.text_input("Enter your activity request:", 
                      placeholder="e.g., Is it safe to play cricket in Delhi tomorrow?")

if st.button("Get Recommendation"):
    if not query:
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Consulting the AI Agents (Planner, Executor, Verifier)..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                response.raise_for_status()
                data = response.json()
                
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("Execution Plan")
                    st.json(data.get("plan", {}))

                with col2:
                    st.subheader("AI Verdict")
                    recommendation = data.get("recommendation", "No recommendation available.")
                    
                    if "YES" in recommendation.upper():
                        st.success(recommendation)
                    elif "NO" in recommendation.upper():
                        st.error(recommendation)
                    else:
                        st.info(recommendation)

                # Usage Stats
                usage = data.get("usage_stats", {})
                if usage:
                    with st.sidebar:
                        st.header("Token Usage")
                        st.metric("Total Tokens", usage.get("total_tokens", 0))
                        st.metric("Prompt Tokens", usage.get("prompt_tokens", 0))
                        st.metric("Response Tokens", usage.get("candidates_tokens", 0))

                with st.expander("Show Full Response Debug Info"):
                    st.json(data)

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the Backend API. Make sure `uvicorn main:app` is running.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Powered by Google Gemini, OpenWeatherMap, & WAQI")
