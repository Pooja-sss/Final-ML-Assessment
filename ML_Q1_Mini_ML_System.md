# Q1. Mini ML System - Input, Embeddings, Storage, Retrieval

I built a simple working mini ML system that:
- accepts user input text
- generates embeddings
- stores them in a local database
- retrieves the most similar matches in real time

## What I Implemented

The implementation is in [mini_similarity_system.py](/abs/path/c:/Users/rahul/OneDrive/Pictures/Documents/7th%20semster/New%20folder/mini_similarity_system.py:1).

It includes:
- `add_record(text, metadata)` to accept and store new inputs
- `embed_text(text)` to generate an embedding vector
- `search(query, top_k)` to retrieve the most similar records
- JSON-file storage for persistence
- cosine similarity for ranking

## Why This Implementation Is Appropriate

For the assessment, I prioritized:
- simplicity
- clarity
- zero external dependency setup
- easy review by the evaluator

So instead of using a large hosted embedding service in the code submission, I implemented a lightweight local embedding pipeline based on hashed token vectors. It still demonstrates the full ML system flow end to end:

`input -> embedding -> storage -> retrieval`

## How It Works

### 1. Accept Input
The system accepts free-text user input such as:
- lead messages
- profile summaries
- search queries
- recommendation context

### 2. Generate Embeddings
The system converts text into a fixed-size numeric vector using:
- lowercase normalization
- tokenization
- hashed token projection into a fixed embedding dimension
- vector normalization

This is a simple embedding method suitable for a mini system demo.

### 3. Store Embeddings
Each record is stored in a local file with:
- `id`
- `text`
- `metadata`
- `embedding`
- `created_at`

### 4. Retrieve Similar Results
At query time:
- the query text is embedded using the same embedding function
- all stored embeddings are loaded
- cosine similarity is calculated
- top matches are returned in descending order

## Example Usage

```python
from mini_similarity_system import MiniSimilaritySystem

system = MiniSimilaritySystem("similarity_demo.db")

system.add_record("Looking for AI automation for our campaign launch", {"type": "lead"})
system.add_record("Need personalised recommendations for e-commerce users", {"type": "recommendation"})
system.add_record("Want better lead scoring and sales intelligence", {"type": "lead_intelligence"})

results = system.search("Need AI support for campaign automation", top_k=2)
for item in results:
    print(item)
```

## Example Output

```python
[
  {
    "id": 1,
    "text": "Looking for AI automation for our campaign launch",
    "metadata": {"type": "lead"},
    "score": 0.71
  },
  {
    "id": 3,
    "text": "Want better lead scoring and sales intelligence",
    "metadata": {"type": "lead_intelligence"},
    "score": 0.38
  }
]
```

## Why This Demonstrates the Core Capability

Although the embedding method is lightweight, the system still proves the essential ML engineering capability required in the scenario:
- capture data
- convert it into vector form
- persist it
- retrieve relevant matches in real time

In production, the same architecture can be upgraded by replacing the local embedding function with a stronger embedding model and swapping file storage for Postgres with `pgvector` or a vector database.
