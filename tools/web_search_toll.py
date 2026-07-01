API_KEY = "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"
from tavily import TavilyClient
from langchain_core.tools import tool

@tool
def web_tool(query: str) -> list:
    client = TavilyClient(API_KEY)
    return client.search(
        query=query,
        search_depth="advanced"
    )["results"]

if __name__ == "__main__":

    query = "How has the semiconductor industry evolved in the last 5 years?"

    results = web_tool(query)

    print(results[0])