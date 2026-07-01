from rag.ddb import query_vector_database

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> list:
    results = query_vector_database(query)
    context = []

    for metadata, chunk, score in results:
        context.append({
            "metadata": metadata,
            "chunk": chunk,
            "score": score
        })
    return context[:top_k]