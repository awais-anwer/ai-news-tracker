# 📰 AI News Summarizer & Topic Tracker

An intelligent news summarization and trend-tracking web app powered by **Google Gemini**, **LangChain**, and **FastAPI**.
It fetches the latest articles on any topic, generates concise summaries, and highlights trending keywords.

---

## 🚀 Features

* **AI-Powered Summaries** – Uses Google Gemini via LangChain to summarize news in 3 crisp bullet points.
* **Per-User Trending Topics** – Tracks trending keywords based only on each user's recent article summaries.
* **Real-Time News Fetching** – Fetches live articles using the NewsAPI.
* **Streamlit Frontend** – Clean and responsive UI for easy interaction.
* **FastAPI Backend** – Async backend for efficient concurrent requests.
* **Dockerized Deployment** – Fully containerized and deployed on [Render](https://render.com) free tier.

---

## 🧠 Tech Stack

| Layer               | Technology                |
| ------------------- | ------------------------- |
| **Frontend**        | Streamlit                 |
| **Backend**         | FastAPI                   |
| **LLM Integration** | LangChain + Google Gemini |
| **News Source**     | NewsAPI                   |
| **Deployment**      | Docker + Render           |

---

## ⚙️ How It Works

1. User enters a topic → app fetches 5 latest related articles from NewsAPI.
2. Each article is summarized by Google Gemini (via LangChain).
3. Summaries are stored temporarily per user (in memory).
4. '/news/trending' analyzes the user's summaries to find top trending topics.

---


## 🌐 Live Demo

* **Backend:** [https://ai-news-tracker.onrender.com/health](https://ai-news-tracker.onrender.com/health)
* **Live:** [https://front-ai-news-tracker.onrender.com](https://front-ai-news-tracker.onrender.com)

---

## 🧩 Example Workflow

1.  Enter a topic → “Artificial Intelligence”
2. The app fetches latest AI-related news
3. Each article is summarized in bullets
4. Sidebar shows trending AI keywords based on your session summaries

---

## 🧠 Key Design Choices

* **Per-User Isolation:** Each user gets a unique session ID → summaries and trends are user-specific.
* **Thread-Safe and Scalable:** Designed for asynchronous, concurrent requests with low resource usage.
* **Future-Ready:** Easily extendable with persistent DB or multi-worker scaling if needed.

---

## 📟 License

MIT License © 2025 [Awais Anwer](https://github.com/awais-anwer)
