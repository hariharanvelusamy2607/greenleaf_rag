import logging
import math
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from huggingface_hub import InferenceClient
from pinecone import Pinecone

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
GEN_MODEL = os.environ.get("GEN_MODEL", "meta-llama/Llama-3.2-3B-Instruct:novita")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX", "greenleaf-rag")
PINECONE_INDEX_HOST = os.environ.get("PINECONE_INDEX_HOST")

if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY is not set.")

if not PINECONE_INDEX_HOST:
    raise RuntimeError("PINECONE_INDEX_HOST is not set. Provide the index host from Pinecone console.")

hf_client = InferenceClient(token=HF_TOKEN)
pinecone = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecone.Index(name=PINECONE_INDEX_NAME, host=PINECONE_INDEX_HOST)

# Using Hugging Face InferenceClient directly instead of OpenAI client to avoid httpx compatibility issues


def split_into_h1_chunks(text: str) -> List[Tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^# .*$", text))
    if not matches:
        cleaned = text.strip()
        return [("", cleaned)] if cleaned else []

    chunks: List[Tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        chunk_text = text[start:end].strip()
        if not chunk_text:
            continue
        header_line = match.group(0).lstrip("#").strip()
        chunks.append((header_line, chunk_text))

    if not chunks:
        cleaned = text.strip()
        if cleaned:
            chunks.append(("", cleaned))
    return chunks


def embed_and_normalize(text: str) -> List[float]:
    raw_result = hf_client.feature_extraction(text, model=EMBED_MODEL)
    if hasattr(raw_result, "tolist"):
        raw_result = raw_result.tolist()
    embedding = raw_result[0] if len(raw_result) and isinstance(raw_result[0], list) else raw_result
    l2_norm = math.sqrt(sum(value * value for value in embedding))
    return [value / l2_norm for value in embedding] if l2_norm else embedding


def ingest_markdown(markdown: str, document_id: Optional[str] = None, namespace: Optional[str] = None) -> List[str]:
    fragments = split_into_h1_chunks(markdown)
    if not fragments:
        raise ValueError("No content to ingest after chunking.")

    base_doc_id = document_id or f"doc-{datetime.utcnow().isoformat()}"
    total_chunks = len(fragments)
    vectors = []
    chunk_ids: List[str] = []

    for idx, (title, chunk_text) in enumerate(fragments, start=1):
        chunk_id = f"{base_doc_id}-chunk-{idx:03d}"
        normalized_embedding = embed_and_normalize(chunk_text)
        metadata = {
            "section_title": title or "untitled",
            "chunk_index": idx,
            "chunk_count": total_chunks,
            "document_id": base_doc_id,
            "created_at": datetime.utcnow().isoformat(),
            "content": chunk_text,
        }
        vectors.append({"id": chunk_id, "values": normalized_embedding, "metadata": metadata})
        chunk_ids.append(chunk_id)

    pinecone_index.upsert(vectors=vectors, namespace=namespace)
    logging.info("Upserted %d chunk(s) into Pinecone (namespace=%s)", len(vectors), namespace or "default")
    return chunk_ids


def query_chunks(question: str, top_k: int = 5, namespace: Optional[str] = None) -> List[Dict]:
    query_embedding = embed_and_normalize(question)
    results = pinecone_index.query(
        namespace=namespace,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
    )
    if not results.matches:
        return []
    formatted = []
    for match in results.matches:
        formatted.append(
            {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata or {},
            }
        )
    return formatted


def format_context(matches: List[Dict]) -> str:
    context_blocks = []
    for idx, match in enumerate(matches, start=1):
        metadata = match.get("metadata", {})
        chunk_id = match.get("id")
        content = metadata.get("content", "")
        context_blocks.append(f"[Chunk {idx} | id={chunk_id}]\n{content}")
    return "\n\n".join(context_blocks)


def answer_question(question: str, top_k: int = 5, namespace: Optional[str] = None) -> Dict:
    matches = query_chunks(question, top_k=top_k, namespace=namespace)
    context_text = format_context(matches)
    assistant_prompt = f"""Imagine you are a character in a medieval game and your name is Eldric Thorne. Your goal is to answer player questions about the game and its world. Use the provided context to answer user questions. If the context does not contain the answer, say you do not know. Your answers should be in first person.

Context:
{context_text}

Question:
{question}
"""

    # Use Hugging Face Inference API directly for chat completion
    messages = [
        {"role": "system", "content": "Answer concisely using the supplied context."},
        {"role": "user", "content": assistant_prompt},
    ]
    
    response = hf_client.chat_completion(
        messages=messages,
        model=GEN_MODEL,
        max_tokens=512,
        temperature=0.7,
    )
    
    answer = response.choices[0].message.content
    logging.info("Generated answer for question '%s'", question)
    return {"answer": answer, "context": context_text, "matches": matches}

