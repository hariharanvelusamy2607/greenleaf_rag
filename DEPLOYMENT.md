# Deployment Guide

## Prerequisites

1. **Hugging Face Inference**  
   - Token with access to `BAAI/bge-small-en-v1.5` and `meta-llama/Llama-3.2-3B-Instruct:novita`.

2. **Pinecone**  
   - Create a Starter project (free) and an index with cosine metric and dimension matching your embedding model (e.g., 384 for `bge-small`).  
   - Note the **API Key**, **Index Name**, and **Index Host** (shown on the index overview page). The host looks like `greenleaf-rag-xxxxxxxx.svc.us-east-1-aws.pinecone.io`.

3. **Render Account**  
   - GitHub repository containing this project.  
   - Billing info only needed if you move beyond the free tier.

## Environment Variables

Set the following both locally (for testing) and inside Render (Dashboard → Service → Environment):

| Variable | Description |
| --- | --- |
| `HF_TOKEN` | Hugging Face Inference token |
| `EMBED_MODEL` *(optional)* | Defaults to `BAAI/bge-small-en-v1.5` |
| `GEN_MODEL` *(optional)* | Defaults to `meta-llama/Llama-3.2-3B-Instruct:novita` |
| `PINECONE_API_KEY` | Pinecone project key |
| `PINECONE_INDEX` | Pinecone index name (default `greenleaf-rag`) |
| `PINECONE_INDEX_HOST` | Full host URL for the index |

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export HF_TOKEN=...
export PINECONE_API_KEY=...
export PINECONE_INDEX_HOST=...
uvicorn main:app --reload
```

- `python test.py` ingests the sample Project Greenleaf markdown into Pinecone.
- `python runtime.py` runs a sample query via the shared pipeline.

## One-Time Migration: ChromaDB → Pinecone

If you have existing embeddings in ChromaDB that you want to migrate to Pinecone (one-time only):

1. Set environment variables:
   ```bash
   export PINECONE_API_KEY="your_pinecone_api_key"
   export PINECONE_INDEX="greenleaf-rag"
   export PINECONE_INDEX_HOST="your-index-host.svc.us-east-1-aws.pinecone.io"
   ```

2. Run the migration script **once** (this is a standalone utility, not part of the deployed app):
   ```bash
   python3 migrate_to_pinecone.py
   ```

   This script reads all embeddings from your local `chroma_db/` directory and uploads them to Pinecone. It will not run automatically when you deploy the app.

3. After migration, you can delete the local `chroma_db/` directory if desired (it's already in `.gitignore`).

## Deploy to Render

### Step 1: Push to GitHub
1. Create a new repository on GitHub (or use an existing one).
2. In your local project directory, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: RAG API with Pinecone"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub details.

### Step 2: Create Render Account
1. Go to [render.com](https://render.com) and sign up (or log in).
2. Connect your GitHub account when prompted (Render needs access to deploy from your repos).

### Step 3: Create Web Service
1. In the Render dashboard, click **New +** (top right).
2. Select **Web Service**.
3. Click **Connect** next to your GitHub account if not already connected.
4. Find and select your repository from the list.
5. Click **Connect**.

### Step 4: Configure Service Settings
1. **Name**: Give your service a name (e.g., `rag-api` or `greenleaf-rag`).
2. **Region**: Choose the closest region to your users (e.g., `Oregon (US West)` or `Frankfurt (EU Central)`).
3. **Branch**: Leave as `main` (or your default branch).
4. **Root Directory**: Leave blank (unless your code is in a subdirectory).
5. **Environment**: Select **Python 3**.
6. **Build Command**: Enter `pip install -r requirements.txt`
7. **Start Command**: Enter `uvicorn main:app --host 0.0.0.0 --port $PORT`
8. **Plan**: Choose **Free** for testing (sleeps after inactivity) or **Starter** ($7/month) for always-on.

### Step 5: Add Environment Variables
1. Scroll down to the **Environment Variables** section.
2. Click **Add Environment Variable** for each of the following:

   | Key | Value |
   | --- | --- |
   | `HF_TOKEN` | Your Hugging Face token (get from https://huggingface.co/settings/tokens) |
   | `PINECONE_API_KEY` | Your Pinecone API key (from Pinecone dashboard → API Keys) |
   | `PINECONE_INDEX` | Your Pinecone index name (e.g., `rag` or `greenleaf-rag`) |
   | `PINECONE_INDEX_HOST` | Your Pinecone index host URL (e.g., `rag-xxxxx.svc.us-east-1-aws.pinecone.io`) |

   Optional (if you want to override defaults):
   - `EMBED_MODEL` (defaults to `BAAI/bge-small-en-v1.5`)
   - `GEN_MODEL` (defaults to `meta-llama/Llama-3.2-3B-Instruct:novita`)

### Step 6: Deploy
1. Scroll to the bottom and click **Create Web Service**.
2. Render will start building your service (this takes 2-5 minutes).
3. Watch the build logs in real-time. You should see:
   - Installing dependencies from `requirements.txt`
   - Starting the uvicorn server
4. Once deployment completes, you'll see a green status and a URL like `https://your-service-name.onrender.com`.

### Step 7: Test the API
1. Visit `https://your-service-name.onrender.com/health` in your browser. You should see `{"status": "ok"}`.
2. Test the query endpoint using curl or Postman:
   ```bash
   curl -X POST https://your-service-name.onrender.com/query \
     -H "Content-Type: application/json" \
     -d '{"question": "What are the races in Project Greenleaf?"}'
   ```

### Step 8: Use in Your Game Engine
- Your API base URL is: `https://your-service-name.onrender.com`
- Call `POST /query` with JSON body: `{"question": "your question here"}`
- The response includes `answer`, `context_chunks`, and metadata.

**Note**: On the free tier, the service sleeps after 15 minutes of inactivity. The first request after sleep may take 30-60 seconds to wake up. Upgrade to Starter plan ($7/month) for always-on service.

## API Endpoints

- `GET /health` – quick status check.
- `POST /ingest` – body: `{ markdown: "...", document_id?: "...", namespace?: "..." }`. Splits content by H1 headers and upserts to Pinecone.
- `POST /query` – body: `{ question: "...", top_k?: 5, namespace?: "..." }`. Retrieves from Pinecone and returns Eldric Thorne’s answer + context snippets.

Use the public Render URL from your game engine to call the `/query` endpoint directly. Add authentication later if needed.

