from fastapi import APIRouter
from pydantic import BaseModel
from google.genai import types
from services.embeddings import get_embedding
from services.pinecone_client import search_chunks

router = APIRouter()

CHAT_MODEL = "gemini-flash-lite-latest"

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_documents(req: QueryRequest):
    from services.embeddings import _get_client  # reuse the same Gemini client

    embedding = get_embedding(req.question)
    results = search_chunks(embedding)

    if not results:
        return {
            "answer": "No relevant documents found. Please upload some documents first.",
            "sources": [],
        }

    context = "\n\n---\n\n".join(r["text"] for r in results)

    response = _get_client().models.generate_content(
        model=CHAT_MODEL,
        contents=(
            f"Here is the relevant content retrieved from the document:\n\n"
            f"{context}\n\n"
            f"Question: {req.question}\n\n"
            f"Please answer based on the document content above."
        ),
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a helpful assistant that answers questions about uploaded documents. "
                "Use the provided context to answer as fully and helpfully as possible. "
                "If the context contains relevant information, use it to give a detailed answer. "
                "Only say you don't know if the context is completely unrelated to the question."
            ),
            max_output_tokens=1024,
        ),
    )

    return {
        "answer": response.text,
        "sources": results,
    }
