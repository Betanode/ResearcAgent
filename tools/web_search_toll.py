from tavily import TavilyClient
from langchain_core.tools import tool

API_KEY = "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"

@tool
def web_tool(query: str) -> list:
    """
    Search the web using Tavily and return relevant search results.

    Args:
        query: User's search query.

    Returns:
        List of search results from Tavily.
    """
    client = TavilyClient(API_KEY)

    return client.search(
        query=query,
        search_depth="advanced"
    )["results"]
