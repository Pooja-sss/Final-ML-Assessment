# Q4. Failure Handling

## 1. Invalid Input

Examples:
- empty string
- only symbols
- extremely long irrelevant text
- wrong data type

### Handling
- validate input at API level
- trim whitespace
- reject empty or malformed requests with clear error messages
- optionally cap maximum input length

### Why
This prevents bad records from entering the embedding and retrieval pipeline.

## 2. Missing Embeddings

This can happen if:
- embedding generation failed
- old records were inserted before embeddings existed
- background worker crashed

### Handling
- mark records with embedding status
- skip missing embeddings during retrieval
- retry embedding generation asynchronously
- alert if missing-embedding rate increases

### Why
The search system should continue working even if some records are incomplete.

## 3. Slow Model Responses

If a hosted embedding model is slow:
- set request timeout
- use retries with limits
- queue non-urgent embedding jobs
- return acknowledgment for async ingestion flows
- cache repeated query embeddings when useful

### Why
This prevents user-facing APIs from hanging.

## 4. Database Failures

Examples:
- connection loss
- write failure
- query timeout

### Handling
- retry transient DB errors
- use connection pooling
- log request ID and failure reason
- return safe API error response
- keep ingestion jobs retryable

### If DB Is Fully Down
- fail gracefully
- avoid corrupt partial writes
- store failed jobs in retry queue or dead-letter queue

## 5. Inconsistent Embedding Versions

If the embedding model changes over time:
- store `embedding_version`
- avoid mixing incompatible embeddings in the same retrieval set without migration
- re-embed old records in batch when upgrading models

## 6. Bad Similarity Results

If retrieval quality appears wrong:
- log query and returned scores
- review false positives and false negatives
- evaluate whether the issue comes from the embedding model, indexing, or preprocessing

## Summary

The system should never assume perfect inputs, perfect models, or perfect infrastructure.

My design principle is:
- validate early
- fail safely
- retry where useful
- degrade gracefully
- keep the system observable
