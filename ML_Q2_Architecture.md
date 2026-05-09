# Q2. Architecture Explanation

## Goal

Design a mini ML system that stores user inputs, generates embeddings, and retrieves the most relevant matches in real time for use cases like:
- personalization
- lead intelligence
- recommendations

## High-Level Architecture

```text
[Client / Form / App / Chat]
            |
            v
      [API Endpoint]
            |
            v
[Validation + Normalization Layer]
            |
            +----------------------+
            |                      |
            v                      v
   [Embedding Generator]      [Input Storage]
            |                      |
            +----------+-----------+
                       |
                       v
         [Vector Storage / Database]
                       |
                       v
              [Similarity Search]
                       |
                       v
                [Top-K Results API]
```

## 1. Embedding Model Choice

### For This Submission
I used a lightweight local hashed-vector embedding approach in Python because:
- it runs without external APIs
- it is easy to understand
- it shows the full pipeline clearly

### For Production
I would use a stronger semantic embedding model such as:
- `text-embedding-3-small` for cost-efficient high-quality embeddings
- or a sentence-transformer model for self-hosted setups

### Why
Production retrieval quality depends heavily on embedding quality. A better embedding model improves semantic matching beyond exact keywords.

## 2. Database Choice

### For This Submission
I used simple file-based local storage because:
- setup is extremely simple
- no infrastructure is required
- it keeps the demo fully runnable in a local environment

### For Production
I would prefer:
- PostgreSQL + `pgvector` for simple scalable production deployments
- or a dedicated vector database for very large-scale retrieval systems

### Why Postgres + pgvector
- familiar operational model
- structured data + vector search in one place
- easier to combine metadata filtering with similarity search

## 3. API Flow

### Insert Flow
1. client sends text input and optional metadata
2. API validates and normalizes input
3. embedding model generates vector
4. record and embedding are stored
5. API returns success with record ID

### Search Flow
1. client sends query text
2. API validates query
3. query embedding is generated
4. similarity search runs against stored vectors
5. top-k results are returned with scores

## 4. Data Pipeline

### Ingestion Stage
- receive input from app, lead form, or recommendation pipeline
- clean text
- remove empty or malformed records

### Embedding Stage
- convert text to vector
- validate vector shape
- store embedding version for future model upgrades

### Retrieval Stage
- embed query
- run similarity search
- return ranked results

### Optional Async Pipeline
For larger systems:
- accept input synchronously
- push embedding generation into a queue
- process embeddings in background workers

## 5. Scaling Approach

### Small Scale
For up to a few thousand records:
- simple DB
- in-process similarity search
- batch reads are acceptable

### Medium Scale
For 10k to 100k+ records:
- move to Postgres with vector indexing
- precompute embeddings
- avoid computing embeddings during retrieval except for the query
- use async workers for ingestion

### Large Scale
For much larger systems:
- dedicated vector DB or sharded vector storage
- ANN indexing
- caching frequent query results
- separate read and write paths

## 6. Practical Production Design

If I were building this for a real product, I would use:
- FastAPI for API layer
- embedding model service
- Postgres + pgvector
- background worker for bulk ingestion
- monitoring for latency and retrieval quality

## Summary

The architecture is intentionally simple:
- clean API
- embedding generation layer
- vector-capable storage
- similarity retrieval service

This design is easy to explain, easy to build, and strong enough to evolve into production.
