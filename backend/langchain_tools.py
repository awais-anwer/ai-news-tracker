import os, requests, re, uuid, threading
from collections import defaultdict, deque
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# ------------------- PER-USER MEMORY STORE ---------------------
# Each user gets their own summary history (max 10 per user)
user_summaries = defaultdict(lambda: deque(maxlen=10))
# Lock for thread safety
summaries_lock = threading.Lock()

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
def summarize_text(text, session_id):
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)
    prompt = PromptTemplate.from_template(
        "Summarize the following news article in 3 concise bullet points:\n\n{text}"
    )
    chain = LLMChain(prompt=prompt, llm=model)
    summary = chain.run({"text": text})
    
    # Save summary for this user's session
    with summaries_lock:
        user_summaries[session_id].append(summary)

    return summary

# ------------------- TRENDING TOPIC EXTRACTOR -------------------------
def extract_keywords(session_id):
    """Extract trending topics only from this user's summaries."""
    with summaries_lock:
        summaries = user_summaries.get(session_id, None)
        if not summaries or len(summaries) == 0:
            return ["No recent summaries available"]
        combined = "\n".join(list(summaries))

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


# ------------------- SESSION ID UTILITY -------------------------
def get_or_create_session_id(request_headers):
    """Generate or read user session ID from frontend."""
    session_id = request_headers.get("X-Session-ID")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id