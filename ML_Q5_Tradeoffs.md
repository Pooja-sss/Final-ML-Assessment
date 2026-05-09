# Q5. Trade-offs

## 1. Simplicity vs Semantic Quality

### Choice
For the implementation, I used a lightweight local embedding method.

### Trade-off
- simpler to run and review
- lower semantic quality than a modern production embedding model

### Why
The assessment asks for clarity over complexity. I wanted a working system with zero setup friction.

## 2. SQLite vs Production Vector Storage

### Choice
I used SQLite in the demo.

### Trade-off
- very easy to run locally
- not ideal for large-scale vector retrieval

### Why
It is enough to prove the end-to-end system. In production, I would replace it with Postgres + `pgvector`.

## 3. Exact Search vs Approximate Search

### Choice
The demo uses direct similarity calculation.

### Trade-off
- easy to understand and verify
- slower at larger scale

### Why
For a mini system, exact search keeps the implementation transparent. At higher scale, I would switch to ANN indexing such as HNSW.

## 4. Sync Simplicity vs Async Robustness

### Choice
The local demo is simple and mostly synchronous.

### Trade-off
- easier to read
- less robust under high traffic or slow model calls

### Why
For production, I would move ingestion and embedding generation to async workers, but for the assessment a simpler flow is easier to review.

## 5. One-System Design vs Specialized Services

### Choice
I kept embedding, storage, and retrieval in one minimal system.

### Trade-off
- lower operational complexity
- less flexibility than separate embedding service, retrieval service, and ingestion workers

### Why
The goal here is a clear and practical MVP, not a fully distributed architecture.

## Final View

The main trade-off I made throughout the design was:

**choose a clean, understandable system that demonstrates the right ML engineering thinking, while clearly showing how it would evolve for production**
