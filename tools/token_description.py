import requests

def token_description(token_id: str = "solana") -> str:
    """
    Retrieve the project description from CoinGecko.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()
        desc = data.get("description", {}).get("en", "")
        if not desc:
            return "No description available."
        # Truncate to 500 chars for readability
        return desc.strip().replace("\r\n", " ")[:500] + "..."
    except Exception as e:
        return f"❌ Description error: {e}"
