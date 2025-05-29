import requests

def token_market_data(token_id: str = "solana") -> str:
    """
    Returns market cap, volume, and 24h price change.
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        res = requests.get(url, params={"vs_currency": "usd", "ids": token_id}, timeout=5)
        res.raise_for_status()
        items = res.json()
        if not items:
            return "No market data found."
        t = items[0]
        return (
            f"*{t['name']}* ({t['symbol'].upper()})\n"
            f"• Price: ${t['current_price']:,}\n"
            f"• Market Cap: ${t['market_cap']:,}\n"
            f"• 24h Vol: ${t['total_volume']:,}\n"
            f"• 24h Change: {t['price_change_percentage_24h']:.2f}%"
        )
    except Exception as e:
        return f"❌ Market data error: {e}"
