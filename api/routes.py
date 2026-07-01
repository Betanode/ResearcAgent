import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException

from rag.loader import convert_pdf_to_markdown
from rag.chunking import divide_document_into_chunks
from rag.ddb import create_vector_database
from agent.executer import run_agent
from api.schemas import QueryRequest, QueryResponse, UploadResponse, IngestRequest

app = FastAPI(title="Research Agent API")

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Research Agent API is running"}


@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, convert it to markdown, chunk it, and store in the vector DB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_name = Path(file.filename).stem

    try:
        create_vector_database(str(save_path), doc_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {e}")

    return UploadResponse(
        message="PDF uploaded and indexed successfully.",
        doc_name=doc_name,
        chunks_inserted=-1,  # ddb.py does not return count; logged internally
    )


@app.post("/ingest", response_model=UploadResponse)
async def ingest_pdf(request: IngestRequest):
    """
    Ingest a PDF from a local server path into the vector database.
    """
    if not Path(request.pdf_path).exists():
        raise HTTPException(status_code=404, detail="PDF path not found on server.")

    try:
        create_vector_database(request.pdf_path, request.doc_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest PDF: {e}")

    return UploadResponse(
        message="PDF ingested and indexed successfully.",
        doc_name=request.doc_name,
        chunks_inserted=-1,
    )


@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Ask the research agent a question. It retrieves from the vector DB and/or the web.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        answer = run_agent(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {e}")

    return QueryResponse(query=request.query, answer=answer)


@app.get("/convert-pdf")
async def convert_pdf(pdf_path: str, output_dir: str = "./data"):
    """
    Convert PDF(s) at the given path to markdown files.
    """
    try:
        generated_files = convert_pdf_to_markdown(pdf_path)
        return {"generated_markdown_files": generated_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/divide-document")
async def divide_document(md_file: str, doc_name: str):
    """
    Divide a markdown file into chunks and return the count.
    """
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()

        chunks = divide_document_into_chunks(md_text, doc_name)

        return {
            "doc_name": doc_name,
            "total_child_chunks": len(chunks),
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {md_file}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
