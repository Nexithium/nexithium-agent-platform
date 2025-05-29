from typing import Callable, List, Dict

# Define a registry for tools
tool_registry: Dict[str, Callable] = {}

def register_tool(name: str):
    """
    Decorator to register a tool function under a specific name.
    """
    def wrapper(func: Callable):
        tool_registry[name] = func
        return func
    return wrapper

def get_tool(name: str) -> Callable:
    if name in tool_registry:
        return tool_registry[name]
    raise ValueError(f"Tool '{name}' not found")

def list_tools() -> List[str]:
    return list(tool_registry.keys())

# Example: dynamic import of tool modules
def load_all_tools():
    from tools.coingecko import get_price
    from tools.google_search import google_search
    from tools.tavily import tavily_news
    from tools.token_trend import token_trend
    from tools.token_description import token_description
    from tools.token_market_data import token_market_data

    register_tool("get_price")(get_price)
    register_tool("google_search")(google_search)
    register_tool("tavily_news")(tavily_news)
    register_tool("token_trend")(token_trend)
    register_tool("token_description")(token_description)
    register_tool("token_market_data")(token_market_data)

    return tool_registry

# Optionally preload on module load
load_all_tools()
