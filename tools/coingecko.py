import requests

def get_price(symbol: str) -> str:
    """
    Fetch current USD price for a token via CoinGecko.
    Usage: get_price("bitcoin") or get_price("BTC")
    """
    token_id = symbol.lower()
    # Mapping common symbols to CoinGecko IDs
    SYMBOL_MAP = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "avax": "avalanche",
        "doge": "dogecoin",
        "link": "chainlink",
        "ada": "cardano",
        "matic": "matic-network",
    }
    token_id = SYMBOL_MAP.get(token_id, token_id)
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": token_id, "vs_currencies": "usd"},
            timeout=5
        )
        res.raise_for_status()
        data = res.json()
        price = data.get(token_id, {}).get("usd")
        if price is not None:
            return f"💰 *{symbol.upper()}* is trading at *${price:.2f} USD*."
        return f"⚠️ Price not available for *{symbol.upper()}*."
    except Exception as e:
        return f"❌ Error fetching price: {e}"
