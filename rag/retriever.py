from rag.vectorDatabase import query_vector_database

def retrieve(query: str , top_k : int = 5):
    results = query_vector_database(query)
    context = []

    for metadata, chunk, score in results:
        context.append({
            "metadata": metadata,
            "chunk": chunk,
            "score": score
        })
    return context[:top_k]