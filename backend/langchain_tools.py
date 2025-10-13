import os, requests, re
from collections import deque
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Store recent summaries
recent_summaries = deque(maxlen=5)

# -------------------------- NEWS FETCHER ---------------------------
def fetch_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&language=en&pageSize=5"
    res = requests.get(url).json()
    return [
        {"title": a["title"], "content": a["description"], "url": a['url']}
        for a in res.get("articles", [])
        if a.get("description")
    ]

# ------------------------- SUMMARIZER -------------------------------
def summarize_text(text):
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
    prompt = PromptTemplate.from_template(
        "Summarize the following news article in 3 concise bullet points:\n\n{text}"
    )
    chain = LLMChain(prompt=prompt, llm=model)
    summary = chain.run({"text": text})
    
    # store this summary for trending analysis
    recent_summaries.append(summary)
    return summary


# ------------------- TRENDING TOPIC EXTRACTOR -------------------------
def extract_keywords():
    """Use Gemini to extract trending topics from the most recent summaries."""
    if not recent_summaries:
        return ["No recent summaries available"]

    # Combine all summaries into a single text
    combined = "\n".join(list(recent_summaries))

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)

    prompt = PromptTemplate.from_template(
        """
        You are an AI news analyst.
        Given the following recent news summaries, identify the 5–7 most trending topics, entities, or themes.
        Return them as a clean, comma-separated list (only the keywords, no extra text).

        News Summaries:
        {text}
        """
    )

    chain = LLMChain(prompt=prompt, llm=model)
    result = chain.run({"text": combined})

    # Clean and split the result into list
    keywords = [kw.strip() for kw in re.split(r",|\n|•|-", result) if kw.strip()]
    # Deduplicate while preserving order
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw.lower() not in seen:
            seen.add(kw.lower())
            unique_keywords.append(kw)

    # Limit to 7 trending topics
    return unique_keywords[:7]
