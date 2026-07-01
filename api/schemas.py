from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    query: str
    answer: str


class UploadResponse(BaseModel):
    message: str
    doc_name: str
    chunks_inserted: int


class IngestRequest(BaseModel):
    pdf_path: str
    doc_name: str
