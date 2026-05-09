# Q6. Evaluating Whether the Similarity System Works Correctly

## 1. Start with a Small Labeled Test Set

I would create a small evaluation dataset with:
- query text
- expected relevant matches
- expected irrelevant matches

Example:
- query: "AI automation for campaign launch"
- relevant: records about campaign automation, marketing AI workflows
- irrelevant: unrelated finance or support records

This gives a basic ground-truth set for testing.

## 2. Retrieval Quality Metrics

### Precision@K
Measures how many of the top-k returned results are actually relevant.

### Recall@K
Measures whether the system is able to find the relevant items within the top-k.

### MRR or Ranking Quality
Checks whether the most relevant result appears near the top.

These are practical metrics for similarity systems.

## 3. Manual Relevance Review

For a small or early-stage system, I would also do manual review of:
- top results for representative queries
- edge-case queries
- failure cases

### Why
Some retrieval errors are obvious to a human even before formal metrics are mature.

## 4. Online Product Evaluation

If this system is used in production for personalization or lead intelligence, I would track downstream metrics such as:
- click-through rate
- conversion rate
- lead qualification usefulness
- response quality feedback

This helps confirm whether better similarity results produce better business outcomes.

## 5. Failure Analysis

When the system performs poorly, I would inspect:
- query text
- returned matches
- similarity scores
- preprocessing behavior
- embedding version

This helps identify whether the problem is caused by:
- weak embeddings
- poor normalization
- wrong indexing configuration
- missing metadata filters

## 6. Regression Testing

Every time the embedding model, preprocessing logic, or indexing strategy changes, I would rerun the evaluation set to ensure quality does not regress.

## 7. What “Working Correctly” Means

I would consider the system correct if:
- semantically similar items rank near the top
- irrelevant items are pushed down
- performance is stable across common query types
- evaluation metrics and manual review both look good

## Summary

I would evaluate the similarity system using a combination of:
- labeled test queries
- Precision@K and Recall@K
- manual review
- downstream product metrics
- regression testing

That gives both technical confidence and business confidence in the system.
