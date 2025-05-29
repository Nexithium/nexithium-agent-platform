import os
import requests

# Placeholder VIP API key for Tavily (crypto news/search)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def tavily_news(query: str = "crypto news") -> str:
    """
    Fetch latest headlines via Tavily (or similar) API.
    """
    if not TAVILY_API_KEY:
        return "⚠️ TAVILY_API_KEY not set in environment."
    try:
        r = requests.get(
            "https://api.tavily.ai/v1/news",
            params={"q": query, "limit": 3},
            headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
            timeout=5
        )
        r.raise_for_status()
        items = r.json().get("articles", [])
        if not items:
            return "📰 No news found."
        reply = "📰 *Recent news:*\n"
        for art in items:
            reply += f"- [{art['title']}]({art['url']})\n"
        return reply
    except Exception as e:
        return f"❌ News error: {e}"
