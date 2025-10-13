import streamlit as st
import requests

st.set_page_config(page_title="AI News Summarizer", layout="wide")

st.title("📰 AI News Summarizer & Topic Tracker")

topic = st.text_input("Enter a topic:", "Artificial Intelligence", key="keyword_input")
if st.button("Fetch Latest News", key="submit_button"):
    with st.spinner("Fetching and summarizing news..."):
        res = requests.post("http://127.0.0.1:8000/news/fetch", json={"topic": topic}).json()
        for article in res["articles"]:
            st.subheader(article["title"])
            summary_res = requests.post("http://127.0.0.1:8000/news/summarize", json={"content": article["content"]}).json()
            st.write(summary_res["summary"])
            st.markdown(f"[Read more]({article['url']})")
            st.divider()

st.sidebar.header("🔥 Trending Topics")
trend_res = requests.get("http://127.0.0.1:8000/news/trending").json()
for kw in trend_res["trending"]:
    st.sidebar.write(f"• {kw}")
