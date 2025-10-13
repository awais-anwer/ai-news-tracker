from fastapi import FastAPI, Request
from dotenv import load_dotenv
from langchain_tools import summarize_text, extract_keywords, fetch_news
from schemas import (
    NewsFetchRequest,
    SummarizeRequest,
    FetchResponse,
    SummarizeResponse,
    TrendingResponse,
    HealthResponse,
)

 
app = FastAPI()
load_dotenv()

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok", "message": "AI News Summarizer backend running"}

@app.post("/news/fetch", response_model=FetchResponse)
async def fetch_news_api(payload: NewsFetchRequest):
    articles = fetch_news(payload.topic)
    return {"articles": articles}

@app.post("/news/summarize", response_model=SummarizeResponse)
async def summarize(payload: SummarizeRequest):
    summary = summarize_text(payload.content)
    return {"summary": summary}

@app.get("/news/trending", response_model=TrendingResponse)
async def trending_keywords():
    keywords = extract_keywords()
    return {"trending": keywords}