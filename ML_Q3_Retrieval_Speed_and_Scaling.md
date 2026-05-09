# Q3. Retrieval Speed, Large-Scale Handling, and Indexing Strategy

## 1. How I Would Optimise Retrieval Speed

### A. Precompute Embeddings
The most important optimization is to generate and store embeddings ahead of time. At search time, only the query embedding should be computed.

### B. Use Fixed-Size Numeric Vectors
Vectors should be stored in a format that supports efficient distance computation and indexing.

### C. Limit Search Space
Use:
- metadata filters
- time filters
- category filters

This reduces the number of candidate vectors before similarity ranking.

### D. Return Top-K Only
Most applications need only a small number of best matches, such as top 5 or top 10.

### E. Cache Frequent Queries
If certain queries repeat often, caching the top results reduces repeated similarity computation.

## 2. Handling 10k+ and 100k+ Records

## 10k+ Records

At this scale:
- Postgres + `pgvector` is usually enough
- exact similarity search may still be acceptable depending on latency requirements
- precomputed embeddings and filtering become important

## 100k+ Records

At this scale:
- approximate nearest neighbor search becomes more valuable
- vector indexes should be used
- ingestion and retrieval should be separated from the API thread
- embedding generation should move to background workers

## Practical Strategy

- 1k to 10k: simple vector storage and direct search is acceptable
- 10k to 100k: use vector indexing in Postgres
- beyond that: consider dedicated ANN-focused storage depending on latency needs

## 3. Indexing Strategy

### Best Practical Choice
For production, I would use `pgvector` with an ANN index such as:
- HNSW for high-quality approximate search

### Why HNSW
- strong balance of speed and recall
- well suited for semantic retrieval
- scalable for larger vector collections

### Alternative
- IVFFlat can also work, especially when tuning latency and memory trade-offs

## 4. Query Strategy

My retrieval flow would be:
1. validate query
2. generate query embedding
3. apply metadata filters if available
4. run indexed similarity search
5. return top-k matches with scores

## 5. Additional Speed Improvements

- store embedding dimension consistently
- avoid repeated JSON parsing in hot paths
- use connection pooling
- batch insert embeddings during ingestion
- keep API responses compact

## 6. Important Design Principle

Retrieval speed is not only about the index.

It also depends on:
- embedding generation latency
- database design
- filtering strategy
- caching
- whether embeddings are precomputed

## Summary

To optimize retrieval speed and support 10k+ or 100k+ records, I would:
- precompute embeddings
- store vectors in Postgres + `pgvector`
- use HNSW indexing
- filter before ranking
- move ingestion to async workers
- use caching for repeated queries

This keeps the system practical, scalable, and easy to operate.
