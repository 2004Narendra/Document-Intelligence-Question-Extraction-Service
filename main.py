from fastapi import FastAPI
from app.api import auth, documents, questions

app = FastAPI(title="Document Intelligence & Question Extraction Service", version="1.0.0")
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(questions.router)


@app.get("/", tags=["System"], include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": "Document Intelligence & Question Extraction Service", "docs": "/docs", "health": "/health"}


@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {"status": "ok"}
