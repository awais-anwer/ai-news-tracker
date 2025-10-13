from fastapi import FastAPI, Request
from dotenv import load_dotenv
from langchain_tools import summarize_text, extract_keywords, fetch_news, get_or_create_session_id
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
async def summarize(request: Request, payload: SummarizeRequest):
    session_id = get_or_create_session_id(request.headers)
    summary = summarize_text(payload.content, session_id=session_id)
    return {"summary": summary, "session_id": session_id}

@app.get("/news/trending", response_model=TrendingResponse)
async def trending_keywords(request: Request):
    session_id = get_or_create_session_id(request.headers)
    keywords = extract_keywords(session_id)
    return {"trending": keywords}
