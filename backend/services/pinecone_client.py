import os
from pinecone import Pinecone
from services.embeddings import get_embedding

def _index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index(os.getenv("PINECONE_INDEX_NAME", "rag-demo"))

def upsert_chunks(chunks: list[dict], filename: str):
    index = _index()
    vectors = []
    for chunk in chunks:
        embedding = get_embedding(chunk["text"])
        vectors.append({
            "id": f"{filename}__{chunk['index']}",
            "values": embedding,
            "metadata": {"text": chunk["text"], "source": filename},
        })
    # Pinecone recommends batches of 100
    for i in range(0, len(vectors), 100):
        index.upsert(vectors=vectors[i : i + 100])

def search_chunks(embedding: list[float], top_k: int = 5) -> list[dict]:
    results = _index().query(vector=embedding, top_k=top_k, include_metadata=True)
    return [
        {
            "text": m.metadata["text"],
            "source": m.metadata["source"],
            "score": round(m.score, 4),
        }
        for m in results.matches
    ]
