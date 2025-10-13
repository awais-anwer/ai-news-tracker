from pydantic import BaseModel, Field
from typing import List, Optional

# ---------- Request Models ----------

class NewsFetchRequest(BaseModel):
    topic: str = Field(default="AI", description="The topic to fetch news about")

class SummarizeRequest(BaseModel):
    content: str = Field(..., description="The news article content to summarize")

# ---------- Response Models ----------

class Article(BaseModel):
    title: str
    content: str
    url: str

class FetchResponse(BaseModel):
    articles: List[Article]

class SummarizeResponse(BaseModel):
    summary: str

class TrendingResponse(BaseModel):
    trending: List[str]

class HealthResponse(BaseModel):
    status: str
    message: str
