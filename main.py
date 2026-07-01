from pathlib import Path
from fastapi import FastAPI

from rag.loader import convert_pdf_to_markdown
from rag.chunking import divide_document_into_chunks

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/convert-pdf")
async def convert_pdf():
    try:
        generated_files = convert_pdf_to_markdown(
            "/Users/abhinavdwivedi/Desktop/ResearchAgent/data"
        )

        return {
            "generated_markdown_files": generated_files
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/divide-document")
async def divide_document():
    try:
        md_file = "/Users/abhinavdwivedi/Desktop/ResearchAgent/data/Attention.md"

        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()

        chunks = divide_document_into_chunks(
            md_text,
            "Attention"
        )

        return {
            "total_child_chunks": chunks
        }

    except Exception as e:
        return {"error": str(e)}