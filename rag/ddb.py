import json
import duckdb

from langchain_huggingface import HuggingFaceEmbeddings

from rag.loader import convert_pdf_to_markdown
from rag.chunking import divide_document_into_chunks


# ---------------------------------------
# Embedding Model
# ---------------------------------------

dense_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------------
# Database Connection
# ---------------------------------------

def get_connection():
    conn = duckdb.connect("research.db")
    conn.execute("LOAD vss")
    return conn


# ---------------------------------------
# Initialize Database
# ---------------------------------------

def initialize_database():

    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER,
            context TEXT,
            embedding DOUBLE[384],
            metadata JSON
        )
        """
    )

    conn.close()


# ---------------------------------------
# Create Vector Database
# ---------------------------------------

def create_vector_database(pdf_path: str, doc_name: str):

    initialize_database()

    conn = get_connection()

    markdown_files = convert_pdf_to_markdown(pdf_path)

    counter = 0

    for md_file in markdown_files:

        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()

        chunks = divide_document_into_chunks(
            md_text,
            doc_name
        )

        for chunk in chunks:

            embedding = dense_embeddings.embed_documents(
                [chunk.page_content]
            )[0]

            embedding = [float(x) for x in embedding]

            conn.execute(
                """
                INSERT INTO documents
                VALUES (?, ?, ?, ?)
                """,
                [
                    counter,
                    chunk.page_content,
                    embedding,
                    json.dumps(chunk.metadata),
                ],
            )

            counter += 1

    conn.close()

    print(f"Inserted {counter} chunks")


# ---------------------------------------
# Query Vector Database
# ---------------------------------------

import numpy as np

def query_vector_database(query: str):

    conn = get_connection()

    query_embedding = np.array(
        dense_embeddings.embed_query(query),
        dtype=np.float32
    ).tolist()

    results = conn.execute(
        """
        SELECT
            metadata,
            context,
            array_cosine_similarity(
                embedding,
                ?
            ) AS score
        FROM documents
        ORDER BY score DESC
        LIMIT 5
        """,
        [query_embedding],
    ).fetchall()

    conn.close()

    return results


# ---------------------------------------
# Testing
# ---------------------------------------

if __name__ == "__main__":

    initialize_database()

    create_vector_database(
        "/Users/abhinavdwivedi/Desktop/ResearchAgent/data",
        "Attention",
    )

    results = query_vector_database(
        "What is this research about?"
    )

    for r in results:

        print("\n----------------")

        print("Metadata:")
        print(r[0])

        print("\nScore:")
        print(r[2])

        print("\nContext:")
        print(r[1])