import requests

def token_trend(token_id: str = "solana") -> str:
    """
    Analyze 2-day trend: % change and direction.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{token_id}/market_chart"
        res = requests.get(url, params={"vs_currency": "usd", "days": 2}, timeout=5)
        res.raise_for_status()
        prices = res.json().get("prices", [])
        if len(prices) < 2:
            return f"No trend data for {token_id}."
        first = prices[0][1]
        last  = prices[-1][1]
        change = (last - first) / first * 100
        direction = "upward 📈" if change > 0 else "downward 📉"
        return f"{token_id.capitalize()} trend over 2 days: {direction} ({change:.2f}%)."
    except Exception as e:
        return f"❌ Trend error: {e}"
