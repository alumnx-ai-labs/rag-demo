from fastapi import APIRouter
from pydantic import BaseModel
from services.embeddings import get_embedding
from services.pinecone_client import search_chunks

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_documents(req: QueryRequest):
    from services.embeddings import _get_client  # reuse the same OpenAI client

    embedding = get_embedding(req.question)
    results = search_chunks(embedding)

    if not results:
        return {
            "answer": "No relevant documents found. Please upload some documents first.",
            "sources": [],
        }

    context = "\n\n---\n\n".join(r["text"] for r in results)

    response = _get_client().chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that answers questions about uploaded documents. "
                    "Use the provided context to answer as fully and helpfully as possible. "
                    "If the context contains relevant information, use it to give a detailed answer. "
                    "Only say you don't know if the context is completely unrelated to the question."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Here is the relevant content retrieved from the document:\n\n"
                    f"{context}\n\n"
                    f"Question: {req.question}\n\n"
                    f"Please answer based on the document content above."
                ),
            },
        ],
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": results,
    }
