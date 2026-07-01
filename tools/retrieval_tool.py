from rag.retriever import retrieve_relevant_chunks
from langchain_core.tools import tool

@tool
def retrieval_tool(query: str) -> list:
    """
    Retrieves relevant chunks of information based on the provided query.

    Args:
        query (str): The user's query for which relevant information is to be retrieved.

    Returns:
        list: A list of relevant chunks of information.
    """
    return retrieve_relevant_chunks(query)