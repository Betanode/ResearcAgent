from langchain_core.tools import tool
from rag.ddb import create_vector_database


@tool
def pdf_tool(pdf_path: str, doc_name: str) -> str:
    """
    Converts a PDF file to markdown, chunks it, and indexes it into the vector database.

    Args:
        pdf_path: Absolute or relative path to the PDF file or directory containing PDFs.
        doc_name: A short name/label to identify this document in the database.

    Returns:
        A confirmation message once indexing is complete.
    """
    create_vector_database(pdf_path, doc_name)
    return f"Successfully ingested '{doc_name}' from '{pdf_path}' into the vector database."


if __name__ == "__main__":
    result = pdf_tool.invoke({
        "pdf_path": "./data",
        "doc_name": "Attention"
    })
    print(result)
