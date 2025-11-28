#!/usr/bin/env python3
"""
Migration script to transfer embeddings from ChromaDB to Pinecone.
Reads all documents from ChromaDB and upserts them to Pinecone.
"""
import logging
import os
from typing import List

import chromadb
from pinecone import Pinecone

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

# Environment variables
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX", "greenleaf-rag")
PINECONE_INDEX_HOST = os.environ.get("PINECONE_INDEX_HOST")
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME", "hf_embeddings")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is required")
if not PINECONE_INDEX_HOST:
    raise ValueError("PINECONE_INDEX_HOST environment variable is required")

# Initialize ChromaDB client
logging.info("Connecting to ChromaDB at %s", CHROMA_DB_PATH)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
try:
    # Try to get the collection directly first
    collection = chroma_client.get_collection(name=CHROMA_COLLECTION_NAME)
except Exception:
    # If it doesn't exist, try get_or_create
    logging.warning("Collection not found, attempting to create...")
    collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

# Initialize Pinecone
logging.info("Connecting to Pinecone index: %s", PINECONE_INDEX_NAME)
pinecone = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecone.Index(name=PINECONE_INDEX_NAME, host=PINECONE_INDEX_HOST)

# Get all data from ChromaDB
logging.info("Fetching all documents from ChromaDB...")
all_data = collection.get(include=["embeddings", "documents", "metadatas"])

ids = all_data.get("ids", [])
embeddings = all_data.get("embeddings", [])
documents = all_data.get("documents", [])
metadatas = all_data.get("metadatas", [])

total_count = len(ids)
logging.info("Found %d document(s) in ChromaDB", total_count)

if total_count == 0:
    logging.warning("No documents found in ChromaDB. Nothing to migrate.")
    exit(0)

# Prepare vectors for Pinecone
vectors = []
for idx, doc_id in enumerate(ids):
    embedding = embeddings[idx] if idx < len(embeddings) else None
    document = documents[idx] if idx < len(documents) else ""
    metadata = metadatas[idx] if idx < len(metadatas) else {}
    
    if not embedding:
        logging.warning("Skipping %s: no embedding found", doc_id)
        continue
    
    # Ensure metadata includes the document content
    pinecone_metadata = metadata.copy()
    if document:
        pinecone_metadata["content"] = document
    
    vectors.append({
        "id": doc_id,
        "values": embedding,
        "metadata": pinecone_metadata
    })

logging.info("Prepared %d vector(s) for Pinecone upsert", len(vectors))

# Upsert to Pinecone in batches (Pinecone recommends batches of 100)
batch_size = 100
success_count = 0

for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    try:
        pinecone_index.upsert(vectors=batch)
        success_count += len(batch)
        logging.info("Upserted batch %d-%d (%d/%d total)", i + 1, min(i + batch_size, len(vectors)), success_count, len(vectors))
    except Exception as e:
        logging.error("Failed to upsert batch %d-%d: %s", i + 1, min(i + batch_size, len(vectors)), e)
        raise

logging.info("Migration complete! Successfully migrated %d/%d document(s) to Pinecone", success_count, total_count)

# Verify by querying Pinecone
logging.info("Verifying migration by checking index stats...")
stats = pinecone_index.describe_index_stats()
logging.info("Pinecone index stats: %s", stats)

