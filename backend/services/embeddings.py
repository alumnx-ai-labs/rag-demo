import os
from google import genai
from google.genai import types

_client = None

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768  # must match the Pinecone index dimension

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def get_embedding(text: str) -> list[float]:
    response = _get_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIM),
    )
    return response.embeddings[0].values
