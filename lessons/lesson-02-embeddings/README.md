# Lesson 2: Understanding Embeddings

## Overview
Learn how text embeddings work and why they're fundamental to Retrieval-Augmented Generation (RAG) systems. Understand how embeddings convert text into numerical vectors that capture semantic meaning, enabling powerful similarity search.

## Learning Objectives
By the end of this lesson, you will:
- Understand what embeddings are and how they represent text
- Generate embeddings using OpenAI's API
- Calculate semantic similarity using cosine similarity
- Normalize vectors for accurate comparison
- Apply embeddings to real product search scenarios
- Understand how embeddings enable multilingual semantic search

## Duration
90 minutes
- Demonstrations: 30 minutes
- Hands-on exercises: 45 minutes
- Verification and review: 15 minutes

## Prerequisites
- ✅ Completed Lesson 1: Environment Setup
- ✅ uv package manager installed (recommended)
- ✅ Python virtual environment activated (`.venv` or `venv`)
- ✅ OpenAI API key configured in `.env`
- ✅ Basic understanding of Python and numpy

## Topics Covered

### 1. **What are Embeddings?**
   - Converting text to numerical vectors
   - Dimensionality (1536 dimensions for text-embedding-3-small)
   - Vector representation of semantic meaning

### 2. **Generating Embeddings**
   - Using OpenAI's `text-embedding-3-small` model
   - API calls and response handling
   - Embedding properties and characteristics

### 3. **Measuring Similarity**
   - Cosine similarity formula and intuition
   - Similarity score ranges (-1 to 1)
   - Comparing different types of text

### 4. **Vector Normalization**
   - Why normalization matters for similarity search
   - L2 norm and unit vectors
   - Implementation in the reference RAG solution

### 5. **Real-World Applications**
   - Product search using semantic similarity
   - Cross-lingual search (Vietnamese ↔ English)
   - Context-aware similarity

## What You'll Create

### Solution Files (Reference)
- ✅ `solution/embeddings_demo.py` - Complete demonstrations
- ✅ `solution/verify.py` - Automated testing script

### Exercise Files (Your Work)
- 📝 `exercises/my_embeddings.py` - Your implementation

## Lesson Structure

### Part 1: Demonstrations (30 min)
Run the solution code to see embeddings in action:

```bash
# Activate your virtual environment first
cd lessons/lesson-02-embeddings
python solution/embeddings_demo.py
```

The demonstration covers:
1. **Basic Embeddings** - Generate and inspect embedding vectors
2. **Product Similarity** - Search for similar products semantically
3. **Normalization** - Why and how to normalize vectors
4. **Real Product Search** - Apply to actual product data

### Part 2: Hands-On Exercises (45 min)
Complete the exercises in `exercises/my_embeddings.py`:

1. **Exercise 1**: Generate embeddings for product descriptions
2. **Exercise 2**: Calculate similarity between query and products
3. **Exercise 3**: Implement and verify vector normalization
4. **Exercise 4**: Build a similarity search function
5. **Bonus**: Explore multilingual semantic search

### Part 3: Verification (15 min)
Test your implementation:

```bash
python solution/verify.py
```

## Key Concepts

### Embedding Vector
A numerical representation of text that captures semantic meaning:
```python
text = "iPhone 15 Pro Max"
embedding = get_embedding(text)
# Returns: [0.023, -0.015, 0.041, ..., 0.008]  # 1536 floats
```

### Cosine Similarity
Measures how similar two vectors are:
```python
similarity = cosine_similarity(vec1, vec2)
# Returns: 0.0 to 1.0 (higher = more similar)
```

**Formula:**
```
cos(θ) = (A · B) / (||A|| × ||B||)
```

### Vector Normalization
Converts vectors to unit length for consistent comparison:
```python
normalized = embedding / np.linalg.norm(embedding)
# Magnitude = 1.0 after normalization
```

## Code Examples

### Generate an Embedding
```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# Use it
embedding = get_embedding("iPhone 15 Pro Max 256GB")
print(f"Dimensions: {len(embedding)}")  # 1536
```

### Calculate Similarity
```python
import numpy as np

def cosine_similarity(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)

    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    return dot_product / (norm_a * norm_b)

# Use it
query_emb = get_embedding("smartphone cao cấp")
product_emb = get_embedding("iPhone 15 Pro Max")
similarity = cosine_similarity(query_emb, product_emb)
print(f"Similarity: {similarity:.4f}")  # e.g., 0.8234
```

### Normalize a Vector
```python
def normalize_embedding(embedding):
    embedding_array = np.array(embedding)
    norm = np.linalg.norm(embedding_array)
    return embedding_array / norm

# Use it (as done in reference solution)
query_embedding = get_embedding("điện thoại giá rẻ")
query_normalized = normalize_embedding(query_embedding)
print(f"Magnitude: {np.linalg.norm(query_normalized)}")  # 1.0
```

## Connection to RAG System

Embeddings are the foundation of the RAG system you're building:

1. **Product Database**: Each product is converted to an embedding
2. **User Query**: User's question is converted to an embedding
3. **Similarity Search**: Find products with highest cosine similarity
4. **Retrieval**: Return the most relevant products to the AI agent
5. **Generation**: Agent uses retrieved products to answer user

**From reference solution** (`final-project/reference-solution/rag.py`):
```python
@function_tool
def rag(query: str) -> str:
    # 1. Get query embedding
    query_embedding = get_embedding(query)

    # 2. Normalize it
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    # 3. Search vector database (ChromaDB)
    search_results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    # 4. Return relevant products
    return search_result
```

## Expected Outcomes

After completing this lesson, you should be able to:

✅ **Understand** how text is converted to numerical vectors
✅ **Generate** embeddings using OpenAI's API
✅ **Calculate** semantic similarity between texts
✅ **Normalize** vectors for accurate comparison
✅ **Apply** embeddings to search and retrieval tasks
✅ **Explain** why embeddings enable cross-lingual search

## Files in This Lesson

```
lesson-02-embeddings/
├── README.md                       # This file
├── instructions.md                 # Step-by-step guide
├── solution/
│   ├── embeddings_demo.py         # Complete demonstrations
│   └── verify.py                  # Verification script
└── exercises/
    └── my_embeddings.py           # Your work here (with TODOs)
```

## Getting Started

1. **Read this README** to understand the objectives
2. **Follow `instructions.md`** for step-by-step guidance
3. **Run the demonstrations** to see embeddings in action
4. **Complete the exercises** in `exercises/my_embeddings.py`
5. **Verify your work** with `solution/verify.py`

## Troubleshooting

### Error: "OpenAI API key not found"
```bash
# Check your .env file
cat ../../.env | grep OPENAI_API_KEY

# Should show: OPENAI_API_KEY=sk-...
```

### Error: "Module 'openai' not found"
```bash
# Make sure virtual environment is activated
# Using uv (recommended, faster):
uv pip install openai python-dotenv numpy

# Or using pip:
pip install openai python-dotenv numpy
```

### Error: "Rate limit exceeded"
- Wait a few seconds and try again
- Check your OpenAI account has credits
- Consider using smaller datasets for testing

### Similarity scores seem wrong
- Make sure you're normalizing vectors
- Check that embeddings are generated correctly (1536 dimensions)
- Verify cosine similarity formula is implemented correctly

For more help, see `docs/troubleshooting.md` in the project root.

## Success Criteria

You've successfully completed this lesson when:

- ✅ All demonstrations run without errors
- ✅ You've implemented all three core functions:
  - `get_embedding()`
  - `cosine_similarity()`
  - `normalize_embedding()`
- ✅ Verification script shows all tests passing
- ✅ You understand how embeddings enable semantic search
- ✅ You can explain the role of embeddings in RAG systems

## Next Steps

After completing this lesson, proceed to:

**→ Lesson 3: Vector Databases (ChromaDB)**
- Store embeddings efficiently
- Perform fast similarity search at scale
- Persist embeddings for the RAG system

## Additional Resources

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Understanding Vector Embeddings](https://www.pinecone.io/learn/vector-embeddings/)
- [Cosine Similarity Explained](https://en.wikipedia.org/wiki/Cosine_similarity)
- Project docs: `docs/architecture.md` - See how embeddings fit in the system

## Learning Tips

💡 **Tip 1**: Run the demonstration code first before doing exercises
💡 **Tip 2**: Print out embedding values to see what they look like
💡 **Tip 3**: Try different texts and observe similarity scores
💡 **Tip 4**: The reference solution is your friend - check it when stuck
💡 **Tip 5**: Embeddings work better than keyword matching for semantic search

---

**Estimated completion time**: 90 minutes
**Difficulty**: ⭐⭐☆☆☆ (Beginner-Intermediate)
**Prerequisites**: Lesson 1 ✅

Good luck! 🚀
