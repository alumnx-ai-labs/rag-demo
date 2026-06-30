import os
import anthropic
from fastapi import APIRouter
from pydantic import BaseModel
from services.embeddings import get_embedding
from services.pinecone_client import search_chunks

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_documents(req: QueryRequest):
    embedding = get_embedding(req.question)
    results = search_chunks(embedding)

    if not results:
        return {
            "answer": "No relevant documents found. Please upload some documents first.",
            "sources": [],
        }

    context = "\n\n---\n\n".join(r["text"] for r in results)

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Answer the question using only the context below. "
                    f"If the answer is not in the context, say \"I don't know based on the provided documents.\"\n\n"
                    f"Context:\n{context}\n\n"
                    f"Question: {req.question}"
                ),
            }
        ],
    )

    return {
        "answer": message.content[0].text,
        "sources": results,
    }
