import os
import streamlit as st
import requests
import uuid

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Generate unique session ID per user (kept in Streamlit session)
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

headers = {"X-Session-ID": st.session_state["session_id"]}

st.set_page_config(page_title="AI News Summarizer", layout="wide")

st.title("📰 AI News Summarizer & Topic Tracker")

topic = st.text_input("Enter a topic:", "Artificial Intelligence")
if st.button("Fetch Latest News"):
    with st.spinner("Fetching and summarizing news..."):
        res = requests.post(f"{BACKEND_URL}/news/fetch", json={"topic": topic}).json()
        for article in res["articles"]:
            st.subheader(article["title"])
            summary_res = requests.post(
                f"{BACKEND_URL}/news/summarize",
                json={"content": article["content"]},
                headers=headers,
            ).json()
            st.write(summary_res["summary"])
            st.markdown(f"[Read more]({article['url']})")
            st.divider()

st.sidebar.header("🔥 Trending Topics")
trend_res = requests.get(f"{BACKEND_URL}/news/trending", headers=headers).json()
for kw in trend_res["trending"]:
    st.sidebar.write(f"• {kw}")
