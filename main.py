from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from rag_pipeline import answer_question, ingest_markdown

app = FastAPI(title="Project Greenleaf RAG API")


class IngestRequest(BaseModel):
    markdown: str
    document_id: str | None = None
    namespace: str | None = None


class IngestResponse(BaseModel):
    chunk_ids: list[str]
    count: int
    document_id: str


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    namespace: str | None = None


class QueryResponse(BaseModel):
    answer: str
    context: str
    sources: list[dict]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    if not req.markdown.strip():
        raise HTTPException(status_code=400, detail="Markdown content is required.")
    chunk_ids = ingest_markdown(req.markdown, document_id=req.document_id, namespace=req.namespace)
    document_id = req.document_id or chunk_ids[0].split("-chunk-")[0]
    return IngestResponse(chunk_ids=chunk_ids, count=len(chunk_ids), document_id=document_id)


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question is required.")
    result = answer_question(req.question, top_k=req.top_k, namespace=req.namespace)
    return QueryResponse(answer=result["answer"], context=result["context"], sources=result["matches"])

