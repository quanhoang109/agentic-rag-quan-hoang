# Lesson 3: Vector Database with ChromaDB - Implementation Plan

**Created:** November 26, 2025
**Status:** 📋 Ready for Implementation
**Based on:** plan.md (lines 211-268) and reference-solution/setup.py

---

## Overview

This lesson teaches students how to use ChromaDB, a vector database, to store and search embeddings efficiently. Students will learn to persist embeddings from Lesson 2 and perform fast similarity searches at scale.

---

## Learning Objectives

By the end of this lesson, students will be able to:
1. Understand vector database concepts and why they're needed for RAG
2. Set up ChromaDB with persistent storage
3. Create and manage collections
4. Insert documents with embeddings and metadata
5. Perform vector similarity searches
6. Update and delete documents
7. Understand the connection between Lesson 2 (embeddings) and Lesson 4 (RAG)

---

## Duration

**Estimated Time:** 1.5 hours
- Part 1: Understanding Vector Databases (15 min)
- Part 2: ChromaDB Setup (15 min)
- Part 3: CRUD Operations (30 min)
- Part 4: Vector Search (20 min)
- Part 5: Exercises (10 min each = 40 min)

---

## Prerequisites

Students should have completed:
- ✅ Lesson 1: Environment Setup
- ✅ Lesson 2: Understanding Embeddings

Students should understand:
- How to generate embeddings using OpenAI API
- What cosine similarity means
- Basic Python (lists, dictionaries, functions)

---

## Topics Covered

### Core Concepts
1. **Vector Database Architecture**
   - Why we need vector databases vs. traditional databases
   - How ChromaDB organizes data (collections, documents, metadata)
   - Persistent vs. in-memory storage

2. **ChromaDB Client**
   - `PersistentClient` for disk storage
   - Collection management (create, get, delete)
   - Document IDs and metadata

3. **CRUD Operations**
   - **Create**: Adding documents with embeddings
   - **Read**: Querying by vector similarity
   - **Update**: Modifying existing documents
   - **Delete**: Removing documents

4. **Vector Search Queries**
   - Query by embedding vectors
   - Top-k results (`n_results` parameter)
   - Filtering with metadata
   - Distance metrics (cosine, L2, inner product)

---

## File Structure

```
lessons/lesson-03-vector-database/
├── README.md                          # Lesson overview (to be created)
├── instructions.md                    # Step-by-step guide (to be created)
├── LESSON_3_PLAN.md                   # This file
├── exercises/
│   ├── my_chromadb.py                 # Student exercises with TODOs
│   └── sample_products.json           # Sample data for exercises
└── solution/
    ├── chromadb_demo.py               # Complete demonstrations
    ├── chromadb_complete.py           # Exercise solutions
    ├── verify.py                      # Automated testing
    ├── setup_sample_data.py           # Load sample data into ChromaDB
    └── sample_products.json           # Sample product data
```

---

## Detailed Content Outline

### Part 1: Understanding Vector Databases (15 min)

**README.md Section: "Why Vector Databases?"**

Explain the limitations of searching embeddings without a database:
```python
# Without vector database (from Lesson 2)
# Problem: Slow for large datasets
query_embedding = get_embedding("smartphone")
for product in products:  # Loop through ALL products
    product_embedding = get_embedding(product)
    similarity = cosine_similarity(query_embedding, product_embedding)
# O(n) complexity - doesn't scale!

# With vector database (ChromaDB)
# Solution: Fast approximate nearest neighbor search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
# O(log n) complexity - scales to millions!
```

**Key Points:**
- Traditional databases: Good for exact matches (SQL WHERE clauses)
- Vector databases: Good for similarity searches (semantic search)
- ChromaDB uses efficient indexing (HNSW algorithm)
- Persistent storage: Data survives restarts

---

### Part 2: ChromaDB Setup (15 min)

**instructions.md Section: "Setting Up ChromaDB"**

#### Step 2.1: Install ChromaDB (already done in Lesson 1)
```bash
# Already in pyproject.toml dependencies
uv sync --no-install-project
```

#### Step 2.2: Create Persistent Client
```python
import chromadb

# In-memory client (data lost on restart)
client = chromadb.Client()  # NOT RECOMMENDED

# Persistent client (data saved to disk)
client = chromadb.PersistentClient(path="db")  # RECOMMENDED
```

#### Step 2.3: Create Collection
```python
# Create new collection
collection = client.create_collection(name="products")

# Get existing collection
collection = client.get_collection(name="products")

# Get or create (safe approach)
collection = client.get_or_create_collection(name="products")
```

**Common Issues:**
- Collection already exists → Use `get_or_create_collection()`
- Invalid collection name → Use `sanitize_collection_name()` helper
- Permission denied → Check directory write permissions

---

### Part 3: CRUD Operations (30 min)

**instructions.md Section: "Working with Documents"**

#### Exercise 1: INSERT - Adding Documents (10 min)

**Goal:** Add product documents with embeddings to ChromaDB

**Template Code (`exercises/my_chromadb.py`):**
```python
import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv
import uuid

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI API (from Lesson 2)."""
    # TODO: Implement this (copy from Lesson 2)
    pass

def exercise_1_insert_documents():
    """
    Exercise 1: Insert documents into ChromaDB

    TODO:
    1. Create ChromaDB persistent client
    2. Create or get collection
    3. Generate embeddings for products
    4. Insert documents with metadata
    """
    print("=" * 70)
    print("EXERCISE 1: Insert Documents into ChromaDB")
    print("=" * 70)

    products = [
        {
            "id": "1",
            "name": "iPhone 15 Pro Max 256GB",
            "price": "29990000",
            "category": "smartphone"
        },
        {
            "id": "2",
            "name": "Samsung Galaxy S24 Ultra 512GB",
            "price": "27990000",
            "category": "smartphone"
        },
        {
            "id": "3",
            "name": "MacBook Pro 14 inch M3",
            "price": "41990000",
            "category": "laptop"
        }
    ]

    # TODO: Step 1 - Create persistent client
    chroma_client = None  # Fix this

    # TODO: Step 2 - Get or create collection
    collection = None  # Fix this

    # TODO: Step 3 - Generate embeddings for each product
    ids = []
    embeddings = []
    metadatas = []

    for product in products:
        # Create searchable text
        text = f"{product['name']} có giá {product['price']} thuộc danh mục {product['category']}"

        # TODO: Generate embedding
        embedding = None  # Fix this

        # Prepare data
        ids.append(product['id'])
        embeddings.append(embedding)
        metadatas.append({
            "name": product['name'],
            "price": product['price'],
            "category": product['category']
        })

    # TODO: Step 4 - Insert documents
    # Hint: collection.add(ids=..., embeddings=..., metadatas=...)

    print(f"✓ Inserted {len(ids)} documents into collection '{collection.name}'")
```

**Solution (`solution/chromadb_complete.py`):**
```python
def exercise_1_insert_documents():
    # ... (same setup)

    # Step 1: Create persistent client
    chroma_client = chromadb.PersistentClient(path="db")

    # Step 2: Get or create collection
    collection = chroma_client.get_or_create_collection(name="products")

    # Step 3: Generate embeddings
    ids = []
    embeddings = []
    metadatas = []

    for product in products:
        text = f"{product['name']} có giá {product['price']} thuộc danh mục {product['category']}"
        embedding = get_embedding(text)

        ids.append(product['id'])
        embeddings.append(embedding)
        metadatas.append({
            "name": product['name'],
            "price": product['price'],
            "category": product['category']
        })

    # Step 4: Insert documents
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✓ Inserted {len(ids)} documents into collection '{collection.name}'")
```

---

#### Exercise 2: QUERY - Vector Search (10 min)

**Goal:** Search for similar products using embeddings

**Template Code:**
```python
def exercise_2_vector_search():
    """
    Exercise 2: Query ChromaDB for similar documents

    TODO:
    1. Get collection from ChromaDB
    2. Generate query embedding
    3. Search for similar documents
    4. Display results
    """
    print("\n" + "=" * 70)
    print("EXERCISE 2: Vector Search")
    print("=" * 70)

    query = "Tôi muốn mua điện thoại iPhone"

    # TODO: Step 1 - Get collection
    chroma_client = None  # Fix this
    collection = None  # Fix this

    # TODO: Step 2 - Generate query embedding
    query_embedding = None  # Fix this

    # TODO: Step 3 - Search for top 3 similar documents
    # Hint: collection.query(query_embeddings=[...], n_results=3)
    results = None  # Fix this

    # TODO: Step 4 - Display results
    print(f"\nQuery: '{query}'")
    print("\nTop 3 results:")
    # Hint: Access results['metadatas'][0], results['distances'][0]
```

**Solution:**
```python
def exercise_2_vector_search():
    query = "Tôi muốn mua điện thoại iPhone"

    # Step 1: Get collection
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="products")

    # Step 2: Generate query embedding
    query_embedding = get_embedding(query)

    # Step 3: Search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Step 4: Display results
    print(f"\nQuery: '{query}'")
    print("\nTop 3 results:")

    for i, (metadata, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0]), 1):
        similarity = 1 - distance  # Convert distance to similarity
        print(f"\n{i}. {metadata['name']}")
        print(f"   Price: {metadata['price']}₫")
        print(f"   Category: {metadata['category']}")
        print(f"   Similarity: {similarity:.4f}")
```

---

#### Exercise 3: UPDATE - Modify Documents (10 min)

**Goal:** Update existing documents in ChromaDB

**Template Code:**
```python
def exercise_3_update_documents():
    """
    Exercise 3: Update existing documents

    TODO:
    1. Get collection
    2. Update metadata for a document
    3. Verify the update
    """
    print("\n" + "=" * 70)
    print("EXERCISE 3: Update Documents")
    print("=" * 70)

    # TODO: Step 1 - Get collection
    chroma_client = None  # Fix this
    collection = None  # Fix this

    # TODO: Step 2 - Update document with id="1"
    # Change price to "28990000" (price drop!)
    # Hint: collection.update(ids=..., metadatas=...)

    # TODO: Step 3 - Query to verify
    # Hint: collection.get(ids=["1"])
```

**Solution:**
```python
def exercise_3_update_documents():
    print("\n" + "=" * 70)
    print("EXERCISE 3: Update Documents")
    print("=" * 70)

    # Step 1: Get collection
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="products")

    # Step 2: Update document
    collection.update(
        ids=["1"],
        metadatas=[{
            "name": "iPhone 15 Pro Max 256GB",
            "price": "28990000",  # Price drop!
            "category": "smartphone"
        }]
    )

    print("✓ Updated product id='1' with new price")

    # Step 3: Verify update
    result = collection.get(ids=["1"])
    print(f"\nUpdated metadata: {result['metadatas'][0]}")
```

---

#### Exercise 4: DELETE - Remove Documents (10 min)

**Goal:** Delete documents from ChromaDB

**Template Code:**
```python
def exercise_4_delete_documents():
    """
    Exercise 4: Delete documents from collection

    TODO:
    1. Get collection
    2. Delete a document by ID
    3. Verify deletion
    """
    print("\n" + "=" * 70)
    print("EXERCISE 4: Delete Documents")
    print("=" * 70)

    # TODO: Step 1 - Get collection
    chroma_client = None  # Fix this
    collection = None  # Fix this

    # TODO: Step 2 - Delete document with id="3"
    # Hint: collection.delete(ids=["3"])

    # TODO: Step 3 - Verify by counting remaining documents
    # Hint: collection.count()
```

**Solution:**
```python
def exercise_4_delete_documents():
    print("\n" + "=" * 70)
    print("EXERCISE 4: Delete Documents")
    print("=" * 70)

    # Step 1: Get collection
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="products")

    print(f"Documents before deletion: {collection.count()}")

    # Step 2: Delete document
    collection.delete(ids=["3"])

    print("✓ Deleted product id='3' (MacBook)")

    # Step 3: Verify
    print(f"Documents after deletion: {collection.count()}")
```

---

### Part 4: Vector Search Deep Dive (20 min)

**instructions.md Section: "Advanced Search Techniques"**

#### Demonstration 1: Search with Metadata Filtering

```python
def demo_metadata_filtering():
    """Show how to filter results by metadata."""
    collection = chroma_client.get_collection(name="products")

    query_embedding = get_embedding("điện thoại")

    # Search only in smartphones category
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        where={"category": "smartphone"}  # Metadata filter!
    )

    print("Results filtered by category='smartphone':")
    for metadata in results['metadatas'][0]:
        print(f"  - {metadata['name']}")
```

#### Demonstration 2: Understanding Distance Metrics

```python
def demo_distance_metrics():
    """Explain ChromaDB distance metrics."""
    print("\nChromaDB Distance Metrics:")
    print("1. cosine (default) - Measures angle between vectors")
    print("   Range: 0 (identical) to 2 (opposite)")
    print("   Use: Most common for text embeddings")

    print("\n2. l2 - Euclidean distance")
    print("   Range: 0 (identical) to ∞")
    print("   Use: When magnitude matters")

    print("\n3. ip - Inner product (dot product)")
    print("   Range: -∞ to ∞")
    print("   Use: With normalized embeddings")

    # Create collection with specific distance metric
    collection = chroma_client.create_collection(
        name="products_l2",
        metadata={"hnsw:space": "l2"}  # Use L2 distance
    )
```

#### Demonstration 3: Batch Operations

```python
def demo_batch_insert():
    """Show how to insert many documents efficiently."""
    import pandas as pd

    # Load CSV
    df = pd.read_csv("../../data/hoanghamobile.csv")

    # Prepare batch data
    ids = [str(i) for i in range(len(df))]
    embeddings = [get_embedding(row['information']) for _, row in df.iterrows()]
    metadatas = [{"name": row['title'], "price": str(row['current_price'])}
                 for _, row in df.iterrows()]

    # Batch insert (much faster than one-by-one)
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✓ Inserted {len(df)} documents in batch")
```

---

### Part 5: Connection to RAG Pipeline (10 min)

**README.md Section: "How This Connects to RAG"**

Show the big picture:

```python
# From Lesson 2: Generate embeddings
query_embedding = get_embedding("Tôi muốn mua iPhone")

# From Lesson 3: Store and search embeddings
collection.add(...)  # Store product embeddings
results = collection.query(query_embeddings=[query_embedding])

# For Lesson 4: Use retrieved context in RAG
retrieved_products = results['metadatas'][0]
context = "\n".join([p['name'] for p in retrieved_products])

# Send to LLM with context
prompt = f"""Based on these products:
{context}

Answer the user's question: Tôi muốn mua iPhone
"""

response = llm.chat.completions.create(...)
```

**Diagram in README.md:**
```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline Flow                         │
└─────────────────────────────────────────────────────────────┘

Step 1 (Lesson 2): Convert text to embeddings
  User Query: "Tôi muốn mua iPhone"
      ↓
  [get_embedding()] → [0.023, -0.015, ..., 0.008]  (1536 dims)

Step 2 (Lesson 3): Search vector database  ← YOU ARE HERE!
  [ChromaDB.query()] → Find 3 most similar products
      ↓
  Results:
    1. iPhone 15 Pro Max - 0.92 similarity
    2. iPhone 15 Pro - 0.89 similarity
    3. iPhone 14 - 0.85 similarity

Step 3 (Lesson 4): Augment with context
  Retrieved Context + Original Query
      ↓
  [LLM] → Generate informed response
      ↓
  "Dựa trên sản phẩm hiện có, iPhone 15 Pro Max..."
```

---

## Verification Script (`solution/verify.py`)

```python
"""
Automated verification for Lesson 3 exercises.
Run: python solution/verify.py
"""

import chromadb
import sys
import os

# Add parent directory to path to import student's code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exercises'))

try:
    from my_chromadb import (
        get_embedding,
        exercise_1_insert_documents,
        exercise_2_vector_search,
        exercise_3_update_documents,
        exercise_4_delete_documents
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you've implemented the required functions in exercises/my_chromadb.py")
    sys.exit(1)

def test_get_embedding():
    """Test 1: Verify get_embedding function works."""
    print("\n" + "=" * 70)
    print("TEST 1: get_embedding()")
    print("=" * 70)

    try:
        embedding = get_embedding("test")

        # Check return type
        assert isinstance(embedding, list), "Should return a list"

        # Check dimensions
        assert len(embedding) == 1536, f"Should be 1536 dimensions, got {len(embedding)}"

        # Check values are floats
        assert all(isinstance(x, float) for x in embedding), "All values should be floats"

        print("✅ PASS: get_embedding() works correctly")
        return True

    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_chromadb_setup():
    """Test 2: Verify ChromaDB client and collection setup."""
    print("\n" + "=" * 70)
    print("TEST 2: ChromaDB Setup")
    print("=" * 70)

    try:
        # Clean up any existing db for testing
        import shutil
        if os.path.exists("db"):
            shutil.rmtree("db")

        # Run exercise 1
        exercise_1_insert_documents()

        # Verify collection exists
        client = chromadb.PersistentClient(path="db")
        collection = client.get_collection(name="products")

        # Verify document count
        count = collection.count()
        assert count == 3, f"Should have 3 documents, got {count}"

        print("✅ PASS: ChromaDB setup and insertion works")
        return True

    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_vector_search():
    """Test 3: Verify vector search works."""
    print("\n" + "=" * 70)
    print("TEST 3: Vector Search")
    print("=" * 70)

    try:
        # This will use the collection from test_chromadb_setup
        exercise_2_vector_search()

        print("✅ PASS: Vector search works")
        return True

    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def test_update_delete():
    """Test 4: Verify update and delete operations."""
    print("\n" + "=" * 70)
    print("TEST 4: Update and Delete")
    print("=" * 70)

    try:
        # Update
        exercise_3_update_documents()

        # Verify update
        client = chromadb.PersistentClient(path="db")
        collection = client.get_collection(name="products")
        result = collection.get(ids=["1"])
        assert result['metadatas'][0]['price'] == "28990000", "Price should be updated"

        # Delete
        exercise_4_delete_documents()

        # Verify deletion
        count = collection.count()
        assert count == 2, f"Should have 2 documents after deletion, got {count}"

        print("✅ PASS: Update and delete work correctly")
        return True

    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "LESSON 3: VERIFICATION TESTS" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")

    tests = [
        test_get_embedding,
        test_chromadb_setup,
        test_vector_search,
        test_update_delete
    ]

    results = [test() for test in tests]

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 70)

    if passed == total:
        print("\n🎉 Congratulations! All tests passed!")
        print("You're ready for Lesson 4: Building Basic RAG Pipeline")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Keep working on the exercises!")

    print("\n")

    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
```

---

## Sample Data Files

### `solution/sample_products.json`
```json
[
    {
        "id": "1",
        "name": "iPhone 15 Pro Max 256GB - Titanium Blue",
        "price": "29990000",
        "category": "smartphone",
        "brand": "Apple",
        "description": "iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch"
    },
    {
        "id": "2",
        "name": "Samsung Galaxy S24 Ultra 512GB - Titanium Gray",
        "price": "27990000",
        "category": "smartphone",
        "brand": "Samsung",
        "description": "Galaxy S24 Ultra với camera 200MP, S Pen tích hợp, màn hình Dynamic AMOLED 6.8 inch"
    },
    {
        "id": "3",
        "name": "MacBook Pro 14 inch M3 - Space Gray",
        "price": "41990000",
        "category": "laptop",
        "brand": "Apple",
        "description": "MacBook Pro 14 inch với chip M3, RAM 16GB, SSD 512GB, màn hình Liquid Retina XDR"
    },
    {
        "id": "4",
        "name": "iPad Pro 11 inch M2 - Silver",
        "price": "21990000",
        "category": "tablet",
        "brand": "Apple",
        "description": "iPad Pro với chip M2, màn hình Liquid Retina 11 inch, hỗ trợ Apple Pencil gen 2"
    },
    {
        "id": "5",
        "name": "AirPods Pro 2nd Generation - White",
        "price": "5990000",
        "category": "audio",
        "brand": "Apple",
        "description": "AirPods Pro thế hệ 2 với chống ồn chủ động, chip H2, hộp sạc MagSafe"
    }
]
```

---

## Key Takeaways for Students

At the end of this lesson, students should understand:

### 1. **Why Vector Databases Matter**
- Traditional databases: Great for exact matches
- Vector databases: Designed for similarity search
- ChromaDB: Fast, persistent, easy to use

### 2. **The CRUD Pattern**
- **Create**: `collection.add(ids, embeddings, metadatas)`
- **Read**: `collection.query(query_embeddings, n_results)`
- **Update**: `collection.update(ids, metadatas)`
- **Delete**: `collection.delete(ids)`

### 3. **Best Practices**
- Always use `PersistentClient` for production
- Use `get_or_create_collection()` to avoid errors
- Batch insert for better performance
- Include useful metadata for filtering
- Generate unique IDs (use uuid)

### 4. **Connection to RAG**
```
Embeddings (Lesson 2) → Vector Database (Lesson 3) → RAG (Lesson 4)
      ↓                          ↓                         ↓
  Convert text              Store & search           Retrieve + Generate
  to numbers                embeddings fast          contextual responses
```

---

## Implementation Checklist

### For Content Developers

- [ ] **README.md** (60 min)
  - [ ] Write "Overview" section
  - [ ] Explain vector database concepts
  - [ ] Include ChromaDB architecture diagram
  - [ ] Add "Why Vector Databases?" section
  - [ ] Show connection to Lesson 2 and Lesson 4
  - [ ] List learning objectives
  - [ ] Add troubleshooting section

- [ ] **instructions.md** (90 min)
  - [ ] Part 1: Understanding Vector Databases (15 min)
  - [ ] Part 2: ChromaDB Setup (15 min)
  - [ ] Part 3: CRUD Operations (30 min)
  - [ ] Part 4: Vector Search (20 min)
  - [ ] Part 5: Connection to RAG (10 min)
  - [ ] Add code examples for each step
  - [ ] Include expected outputs
  - [ ] Add common errors and fixes

- [ ] **exercises/my_chromadb.py** (45 min)
  - [ ] Import statements and setup
  - [ ] `get_embedding()` function (reuse from Lesson 2)
  - [ ] Exercise 1: Insert documents with TODOs
  - [ ] Exercise 2: Vector search with TODOs
  - [ ] Exercise 3: Update documents with TODOs
  - [ ] Exercise 4: Delete documents with TODOs
  - [ ] Helper functions (sanitize_collection_name, etc.)
  - [ ] Main function to run all exercises

- [ ] **solution/chromadb_demo.py** (60 min)
  - [ ] Demo 1: Basic ChromaDB setup
  - [ ] Demo 2: Metadata filtering
  - [ ] Demo 3: Distance metrics comparison
  - [ ] Demo 4: Batch operations with real data
  - [ ] Demo 5: Connection to RAG pipeline preview

- [ ] **solution/chromadb_complete.py** (45 min)
  - [ ] Complete solution for Exercise 1
  - [ ] Complete solution for Exercise 2
  - [ ] Complete solution for Exercise 3
  - [ ] Complete solution for Exercise 4
  - [ ] Well-commented code
  - [ ] Best practices demonstrated

- [ ] **solution/verify.py** (30 min)
  - [ ] Test 1: get_embedding() function
  - [ ] Test 2: ChromaDB setup and insertion
  - [ ] Test 3: Vector search
  - [ ] Test 4: Update and delete operations
  - [ ] Clear pass/fail messages
  - [ ] Helpful error messages

- [ ] **solution/setup_sample_data.py** (20 min)
  - [ ] Load sample_products.json
  - [ ] Generate embeddings
  - [ ] Insert into ChromaDB
  - [ ] Print confirmation

- [ ] **Data Files** (15 min)
  - [ ] Create sample_products.json (5 products)
  - [ ] Copy to exercises/ directory

---

## Success Criteria

Students successfully complete Lesson 3 when they can:

1. ✅ Explain why vector databases are needed for RAG systems
2. ✅ Create a persistent ChromaDB client
3. ✅ Insert documents with embeddings and metadata
4. ✅ Perform vector similarity searches
5. ✅ Update and delete documents
6. ✅ Pass all verification tests (`verify.py`)
7. ✅ Understand how this connects to the RAG pipeline

---

## Estimated Development Time

| Task | Time | Status |
|------|------|--------|
| Planning (this document) | 2 hours | ✅ Complete |
| README.md | 1 hour | 📋 Pending |
| instructions.md | 1.5 hours | 📋 Pending |
| exercises/my_chromadb.py | 45 min | 📋 Pending |
| solution/chromadb_demo.py | 1 hour | 📋 Pending |
| solution/chromadb_complete.py | 45 min | 📋 Pending |
| solution/verify.py | 30 min | 📋 Pending |
| solution/setup_sample_data.py | 20 min | 📋 Pending |
| Data files (JSON) | 15 min | 📋 Pending |
| Testing & refinement | 1 hour | 📋 Pending |
| **Total** | **~9 hours** | **0% Complete** |

---

## Next Steps

1. **Immediate**: Create README.md and instructions.md
2. **Then**: Implement exercise and solution files
3. **Finally**: Test everything with verify.py
4. **After**: Get user feedback and refine

---

**Status:** 📋 Ready for Implementation
**Priority:** High (next lesson in sequence)
**Depends On:** Lessons 1-2 (complete)
**Required For:** Lesson 4 (Basic RAG Pipeline)
