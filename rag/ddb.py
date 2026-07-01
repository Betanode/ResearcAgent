import duckdb
import json

from rag.loader import convert_pdf_to_markdown
from rag.chunking import divide_document_into_chunks
from langchain_huggingface import HuggingFaceEmbeddings


conn = duckdb.connect("research.db")


conn.execute("INSTALL vss;")
conn.execute("LOAD vss;")


conn.execute("""
DROP TABLE IF EXISTS documents
""")


conn.execute("""
CREATE TABLE documents (
    id INTEGER,
    context TEXT,
    embedding FLOAT[384],
    metadata JSON
)
""")


dense_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



def create_vector_database(pdf_path: str, doc_name: str):


    # PDF -> markdown
    markdown_files = convert_pdf_to_markdown(pdf_path)


    counter = 0


    for md_file in markdown_files:


        with open(md_file, "r", encoding="utf-8") as f:
            md_text = f.read()


        # markdown -> chunks
        chunks = divide_document_into_chunks(
            md_text,
            doc_name
        )


        for chunk in chunks:


            embedding = dense_embeddings.embed_documents(
                [
                    chunk.page_content
                ]
            )[0]


            embedding = [
                float(x)
                for x in embedding
            ]


            conn.execute(
                """
                INSERT INTO documents
                VALUES (?, ?, ?, ?)
                """,
                [
                    counter,
                    chunk.page_content,
                    embedding,
                    json.dumps(chunk.metadata)
                ]
            )


            counter += 1


    print(f"Inserted {counter} chunks")




def query_vector_database(query: str):


    query_embedding = dense_embeddings.embed_query(query)


    result = conn.execute(
        """
        SELECT
            metadata,
            context,
            array_cosine_similarity(
                embedding,
                CAST(? AS FLOAT[384])
            ) AS score

        FROM documents

        ORDER BY score DESC

        LIMIT 5
        """,
        [
            query_embedding
        ]
    ).fetchall()


    return result




if __name__ == "__main__":


    create_vector_database(
        "/Users/abhinavdwivedi/Desktop/ResearchAgent/data",
        "Attention"
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