from fastapi import APIRouter, UploadFile, File, HTTPException
from services.document_processor import process_document
from services.pinecone_client import upsert_chunks

router = APIRouter()

ALLOWED_TYPES = {"application/pdf", "text/plain"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")

    content = await file.read()
    chunks = process_document(content, file.filename, file.content_type)

    if not chunks:
        raise HTTPException(status_code=400, detail="Could not extract text from the document.")

    upsert_chunks(chunks, file.filename)
    return {"message": f"Uploaded '{file.filename}'", "chunks": len(chunks)}
