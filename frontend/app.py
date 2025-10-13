import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
# Get backend URL from environment variable (Render) or fallback to localhost for local dev
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI News Summarizer", layout="wide")

st.title("📰 Awais' AI News Summarizer & Topic Tracker")

topic = st.text_input("Enter a topic:", "Artificial Intelligence", key="keyword_input")
if st.button("Fetch Latest News", key="submit_button"):
    with st.spinner("Fetching and summarizing news..."):
        res = requests.post(f"{BACKEND_URL}/news/fetch", json={"topic": topic}).json()
        for article in res["articles"]:
            st.subheader(article["title"])
            summary_res = requests.post(f"{BACKEND_URL}/news/summarize", json={"content": article["content"]}).json()
            st.write(summary_res["summary"])
            st.markdown(f"[Read more]({article['url']})")
            st.divider()

st.sidebar.header("🔥 Trending Topics")
trend_res = requests.get(f"{BACKEND_URL}/news/trending").json()
for kw in trend_res["trending"]:
    st.sidebar.write(f"• {kw}")
