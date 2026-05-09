import streamlit as st
import requests

API_URL = "http://localhost:8000"


def fetch_analysis(ticker: str) -> dict:
    response = requests.get(
        f"{API_URL}/api/analyze/{ticker}",
        timeout=30
    )

    response.raise_for_status()

    return response.json()


st.title("AI Multi-Agent Financial Market Research")

ticker = st.text_input("Ticker", "NVDA")

if st.button("Analyze"):

    with st.spinner("Running multi-agent analysis..."):

        try:
            data = fetch_analysis(ticker)

            st.success("Analysis completed")
            st.json(data)

        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")