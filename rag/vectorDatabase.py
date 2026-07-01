import duckdb
from rag.chunking import divide_document_into_chunks
from langchain_huggingface import HuggingFaceEmbeddings
conn = duckdb.connect("research.db")
import json


conn.execute("""
             INSTALL vss;
             LOAD vss;
             """)

conn.execute(
    """
    CREATE TABLE IF NOT EXISTS documents (
    id INTEGER,
    context TEXT,
    embedding FLOAT[384],
    metadata JSON
    """
)


dense_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def create_vector_database(file_path: str, doc_name: str):
    chunks = divide_document_into_chunks(file_path, doc_name)

    for i,chunk in enumerate(chunks):
        embedding = dense_embeddings.embed_documents([chunk.page_content])[0]

        conn.execute(
            """
            INSERT INTO documents
            VALUES(?,?,?,?)
            """,[
                i,
                chunk.page_content,
                embedding,
                json.dumps(chunk.metadata)
            ]
        )

def query_vector_database(query: str):
    query_embed = dense_embeddings.embed_query(query)
    result = conn.execute(
        """
            SELECT metadata, context,
            array_cosine_similarity(embedding, ?) as score
            FROM documents
            ORDER BY score DESC
        """,[
            query_embed
        ]
    ).fetchall()
    return result

def delete_vector_database():
    conn.execute(
        """
        DROP TABLE IF EXISTS documents
        """
    )