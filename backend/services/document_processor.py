import io
from pypdf import PdfReader

CHUNK_SIZE = 500   # words per chunk
OVERLAP = 50       # words overlap between chunks

def _chunk_text(text: str) -> list[str]:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + CHUNK_SIZE]))
        i += CHUNK_SIZE - OVERLAP
    return chunks

def process_document(content: bytes, filename: str, content_type: str) -> list[dict]:
    if content_type == "application/pdf":
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(
            page.extract_text() for page in reader.pages if page.extract_text()
        )
    else:
        text = content.decode("utf-8", errors="replace")

    chunks = _chunk_text(text)
    return [{"text": chunk, "index": i} for i, chunk in enumerate(chunks) if chunk.strip()]
