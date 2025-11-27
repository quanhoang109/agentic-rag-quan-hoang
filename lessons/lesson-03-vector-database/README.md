# Lesson 3: Vector Database with ChromaDB

## Overview

Learn how to use ChromaDB, a powerful vector database, to store and search embeddings at scale. This lesson bridges the gap between generating embeddings (Lesson 2) and building a complete RAG system (Lesson 4).

## Learning Objectives

By the end of this lesson, you will:
- Understand why vector databases are essential for RAG systems
- Set up ChromaDB with persistent storage
- Perform CRUD operations (Create, Read, Update, Delete) on vector data
- Execute fast similarity searches across thousands of documents
- Prepare for building the complete RAG pipeline in Lesson 4

## Duration

**Estimated Time:** 1.5 hours
- Understanding concepts: 15 minutes
- Setup and demos: 20 minutes
- Hands-on exercises: 40 minutes
- Verification: 15 minutes

## Prerequisites

You should have completed:
- ✅ Lesson 1: Environment Setup (uv, API keys, dependencies)
- ✅ Lesson 2: Understanding Embeddings (generate embeddings, cosine similarity)

You should be comfortable with:
- Python basics (lists, dictionaries, functions)
- Generating embeddings using OpenAI API
- Understanding what vector similarity means

## Topics Covered

### 1. Vector Database Fundamentals
- Traditional databases vs. vector databases
- Why embeddings need specialized storage
- Approximate Nearest Neighbor (ANN) search
- ChromaDB architecture and indexing (HNSW)

### 2. ChromaDB Setup
- Persistent vs. in-memory clients
- Collection management
- Metadata and document IDs
- Best practices for production use

### 3. CRUD Operations
- **Create**: Insert documents with embeddings
- **Read**: Query by vector similarity
- **Update**: Modify existing documents
- **Delete**: Remove documents from collections

### 4. Advanced Queries
- Top-k similarity search
- Metadata filtering
- Distance metrics (cosine, L2, inner product)
- Batch operations for performance

## What You'll Build

By the end of this lesson, you'll have:

1. **A persistent vector database** with ChromaDB storing product embeddings
2. **CRUD functions** to manage vector data
3. **Similarity search** that finds relevant products in milliseconds
4. **Understanding** of how this enables the RAG pipeline

## Files in This Lesson

```
lesson-03-vector-database/
├── README.md                          # This overview
├── instructions.md                    # Step-by-step guide
├── LESSON_3_PLAN.md                   # Implementation plan
├── exercises/
│   ├── my_chromadb.py                 # Your exercises (with TODOs)
│   └── sample_products.json           # Sample data
└── solution/
    ├── chromadb_demo.py               # Demonstrations
    ├── chromadb_complete.py           # Exercise solutions
    ├── verify.py                      # Automated testing
    ├── setup_sample_data.py           # Data loader
    └── sample_products.json           # Sample data
```

## Why Vector Databases?

### The Problem with Simple Search

In Lesson 2, you learned to search by looping through all products:

```python
# Lesson 2 approach: Linear search (slow!)
query_embedding = get_embedding("smartphone")

best_match = None
best_similarity = -1

for product in products:  # O(n) - loops through EVERY product
    product_embedding = get_embedding(product)
    similarity = cosine_similarity(query_embedding, product_embedding)

    if similarity > best_similarity:
        best_similarity = similarity
        best_match = product

# Problem: Gets slower as dataset grows!
# 100 products → 100 comparisons
# 10,000 products → 10,000 comparisons
# 1,000,000 products → 1,000,000 comparisons (too slow!)
```

### The Solution: Vector Databases

Vector databases like ChromaDB use smart indexing:

```python
# ChromaDB approach: Indexed search (fast!)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

# Benefit: Scales to millions of documents!
# Uses HNSW (Hierarchical Navigable Small World) algorithm
# O(log n) complexity instead of O(n)
# 100 products → ~7 comparisons
# 10,000 products → ~13 comparisons
# 1,000,000 products → ~20 comparisons (fast!)
```

**Speed Comparison:**
- 10,000 products with linear search: **~2 seconds**
- 10,000 products with ChromaDB: **~20 milliseconds** (100x faster!)

## How This Connects to RAG

```
┌─────────────────────────────────────────────────────────────┐
│                  RAG Pipeline Overview                       │
└─────────────────────────────────────────────────────────────┘

Lesson 2: Embeddings          Lesson 3: Vector DB         Lesson 4: RAG
     ↓                              ↓                          ↓
┌──────────────┐            ┌──────────────┐          ┌──────────────┐
│ Convert text │            │ Store & find │          │ Retrieve +   │
│ to numbers   │  ─────→    │ similar docs │  ─────→  │ Generate     │
│ (vectors)    │            │ efficiently  │          │ response     │
└──────────────┘            └──────────────┘          └──────────────┘

Example Flow:
1. User: "Tôi muốn mua iPhone"
2. [Embedding] → [0.023, -0.015, ..., 0.008]
3. [ChromaDB] → Find 3 most similar products
4. [LLM] → Generate answer using retrieved context
```

**You are here:** Learning how to efficiently store and retrieve the context that makes RAG work!

## Key Concepts

### 1. Collections

Collections in ChromaDB are like tables in a traditional database:

```python
# Create a collection for products
collection = client.create_collection(name="products")

# Each collection stores:
# - Document IDs (unique identifiers)
# - Embeddings (vector representations)
# - Metadata (additional information like price, category)
```

### 2. Persistent Storage

Data survives restarts:

```python
# In-memory (data lost on restart) ❌
client = chromadb.Client()

# Persistent (data saved to disk) ✅
client = chromadb.PersistentClient(path="db")
```

### 3. Distance Metrics

How similarity is calculated:

- **Cosine** (default): Measures angle between vectors (0 = identical, 2 = opposite)
- **L2**: Euclidean distance (0 = identical, ∞ = far apart)
- **Inner Product**: Dot product (higher = more similar)

For text embeddings, **cosine** is the best choice!

### 4. Metadata Filtering

Filter results by attributes:

```python
# Find smartphones under 20 million VND
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={
        "$and": [
            {"category": "smartphone"},
            {"price": {"$lt": "20000000"}}
        ]
    }
)
```

## Getting Started

Ready to dive in? Open [instructions.md](instructions.md) for the complete step-by-step guide!

## Success Criteria

You've successfully completed this lesson when you can:

1. ✅ Explain why vector databases are needed for RAG
2. ✅ Create a ChromaDB persistent client
3. ✅ Insert documents with embeddings and metadata
4. ✅ Search for similar documents using vector similarity
5. ✅ Update and delete documents
6. ✅ Pass all verification tests (`python solution/verify.py`)
7. ✅ Understand how this enables the RAG pipeline

## What's Next?

After completing this lesson:

- **Lesson 4**: Build a complete RAG pipeline using ChromaDB
- **Lesson 5**: Add AI agents using OpenAI Agents SDK
- **Lesson 6**: Create multi-agent systems with specialized roles

## Troubleshooting

### Common Issues

**Issue: "Collection already exists"**
```python
# Solution: Use get_or_create_collection()
collection = client.get_or_create_collection(name="products")
```

**Issue: "No module named 'chromadb'"**
```bash
# Solution: Install dependencies
uv sync --no-install-project
```

**Issue: "Permission denied" when creating db/ directory**
```bash
# Solution: Check directory permissions
mkdir db
chmod 755 db
```

**Issue: Slow search performance**
- Check if using `PersistentClient` (not in-memory)
- Verify embeddings are normalized
- Consider reducing `n_results` parameter

For more help, see [docs/troubleshooting.md](../../docs/troubleshooting.md)

## Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [HNSW Algorithm Explained](https://arxiv.org/abs/1603.09320)
- [Vector Database Comparison](https://benchmark.vectorview.ai/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)

---

**Ready to start?** Head to [instructions.md](instructions.md) for hands-on learning!
