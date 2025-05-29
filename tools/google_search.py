import os
import requests

# This example uses Serper.dev as a Google-search proxy. Sign up for an API key!
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def google_search(query: str) -> str:
    """
    Return top-3 organic results from a Google-like search.
    """
    if not SERPER_API_KEY:
        return "⚠️ SERPER_API_KEY not set in environment."
    try:
        r = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY},
            json={"q": query},
            timeout=5
        )
        r.raise_for_status()
        results = r.json().get("organic", [])[:3]
        if not results:
            return "🔍 No results found."
        reply = "📄 *Top search results:*\n"
        for item in results:
            title = item.get("title")
            link  = item.get("link")
            reply += f"- [{title}]({link})\n"
        return reply
    except Exception as e:
        return f"❌ Search error: {e}"
