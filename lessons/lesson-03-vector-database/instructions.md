# Lesson 3: Vector Database with ChromaDB - Step-by-Step Instructions

## Introduction

Welcome to Lesson 3! You've learned how to generate embeddings in Lesson 2. Now you'll learn how to store and search them efficiently using ChromaDB, a vector database designed for semantic search.

By the end of this lesson, you'll understand how vector databases enable fast similarity search at scale - a critical component of RAG systems.

## What You'll Build

You'll implement four core operations that power the RAG system:
1. `INSERT` - Add products with embeddings to ChromaDB
2. `QUERY` - Search for similar products using vector similarity
3. `UPDATE` - Modify existing product information
4. `DELETE` - Remove products from the database

## Step 1: Setup and Preparation (10 minutes)

### 1.1 Navigate to Lesson Directory

```bash
cd lessons/lesson-03-vector-database
```

### 1.2 Verify Environment

Make sure your virtual environment is activated and dependencies are installed:

```bash
# Activate virtual environment (if not already active)
# On Windows:
# .venv\Scripts\activate
# On Mac/Linux:
# source .venv/bin/activate

# Verify packages
python -c "import chromadb; import openai; print('✓ Packages ready')"

# If packages not installed:
# uv sync --no-install-project  # Installs all dependencies from pyproject.toml
```

### 1.3 Check API Key

```bash
# Verify OpenAI API key is set
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✓ API key loaded' if os.getenv('OPENAI_API_KEY') else '✗ API key missing')"
```

If you see "API key missing", make sure you have a `.env` file in the project root with:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## Step 2: Run the Demonstrations (30 minutes)

Before writing code, let's see ChromaDB in action.

### 2.1 Run the Demo Script

```bash
python solution/chromadb_demo.py
```

**What to observe:**

#### Demonstration 1: Basic ChromaDB Setup
- How to create a persistent client
- Creating collections
- Understanding document structure (IDs, embeddings, metadata)
- Inserting documents

#### Demonstration 2: Vector Similarity Search
- Querying with embeddings
- Top-k results (`n_results` parameter)
- Distance vs. similarity scores
- How ChromaDB ranks results

#### Demonstration 3: Metadata Filtering
- Filtering by category (e.g., only smartphones)
- Filtering by price range
- Combining multiple filters with `$and`, `$or`
- When to use metadata filters

#### Demonstration 4: Distance Metrics
- Cosine distance (default, best for text)
- L2 distance (Euclidean)
- Inner product
- Comparing results with different metrics

#### Demonstration 5: Batch Operations
- Loading data from CSV
- Batch inserting thousands of documents
- Performance optimization tips
- Preview of RAG pipeline connection

### 2.2 Key Takeaways

After running the demos, you should understand:
- ✅ ChromaDB uses `PersistentClient` to save data to disk
- ✅ Collections store documents with IDs, embeddings, and metadata
- ✅ `collection.query()` finds similar documents fast (O(log n))
- ✅ Metadata filtering narrows results before similarity search
- ✅ Batch operations are much faster than one-by-one inserts

## Step 3: Implement Core Functions (60 minutes)

Now it's your turn! Open `exercises/my_chromadb.py` in your code editor.

### 3.1 Reuse Embedding Function from Lesson 2 (5 min)

**Location:** Line ~20 in `exercises/my_chromadb.py`

**Task:** Copy your `get_embedding()` function from Lesson 2.

**Code:**
```python
def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Generate embedding using OpenAI API (from Lesson 2)."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
```

**How to test:**
```python
# Add at bottom temporarily
if __name__ == "__main__":
    embedding = get_embedding("test")
    print(f"Dimension: {len(embedding)}")  # Should be 1536
```

---

### 3.2 Exercise 1: INSERT Documents (15 min)

**Location:** `exercise_1_insert_documents()` function

**Goal:** Add product documents to ChromaDB with embeddings and metadata.

**What you'll do:**
1. Create a ChromaDB persistent client
2. Create or get a collection
3. Generate embeddings for each product
4. Insert documents with IDs, embeddings, and metadata

**Template Code (with TODOs):**
```python
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
    chroma_client = None  # Fix: chromadb.PersistentClient(path="db")

    # TODO: Step 2 - Get or create collection
    collection = None  # Fix: chroma_client.get_or_create_collection(name="products")

    # TODO: Step 3 - Generate embeddings for each product
    ids = []
    embeddings = []
    metadatas = []

    for product in products:
        # Create searchable text
        text = f"{product['name']} có giá {product['price']} thuộc danh mục {product['category']}"

        # TODO: Generate embedding
        embedding = None  # Fix: get_embedding(text)

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

**Implementation Steps:**

**Step 1:** Create persistent client
```python
chroma_client = chromadb.PersistentClient(path="db")
```

**Why persistent?**
- Data saved to disk in `db/` directory
- Survives program restarts
- Production-ready approach

**Step 2:** Get or create collection
```python
collection = chroma_client.get_or_create_collection(name="products")
```

**Why `get_or_create`?**
- If collection exists: reuses it
- If collection doesn't exist: creates it
- Prevents "collection already exists" errors

**Step 3:** Generate embeddings (already in loop)
```python
embedding = get_embedding(text)
```

**Step 4:** Insert documents
```python
collection.add(
    ids=ids,
    embeddings=embeddings,
    metadatas=metadatas
)
```

**Expected output:**
```
======================================================================
EXERCISE 1: Insert Documents into ChromaDB
======================================================================
✓ Inserted 3 documents into collection 'products'
```

**Verify it worked:**
```python
# Add this after insertion
print(f"Total documents in collection: {collection.count()}")  # Should be 3
```

---

### 3.3 Exercise 2: QUERY with Vector Search (15 min)

**Location:** `exercise_2_vector_search()` function

**Goal:** Search for products similar to a Vietnamese query using vector similarity.

**What you'll do:**
1. Get the collection from ChromaDB
2. Generate embedding for the search query
3. Use `collection.query()` to find similar documents
4. Display results with similarity scores

**Implementation Steps:**

**Step 1:** Get collection
```python
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_collection(name="products")
```

**Note:** Use `get_collection()` (not `get_or_create`) since we know it exists from Exercise 1.

**Step 2:** Generate query embedding
```python
query_embedding = get_embedding(query)
```

**Step 3:** Search with ChromaDB
```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
```

**Important:** `query_embeddings` takes a **list of embeddings**, even if you only have one query!

**Step 4:** Display results
```python
print(f"\nQuery: '{query}'")
print("\nTop 3 results:")

for i, (metadata, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0]), 1):
    similarity = 1 - distance  # Convert distance to similarity
    print(f"\n{i}. {metadata['name']}")
    print(f"   Price: {metadata['price']}₫")
    print(f"   Category: {metadata['category']}")
    print(f"   Similarity: {similarity:.4f}")
```

**Expected output:**
```
======================================================================
EXERCISE 2: Vector Search
======================================================================

Query: 'Tôi muốn mua điện thoại iPhone'

Top 3 results:

1. iPhone 15 Pro Max 256GB
   Price: 29990000₫
   Category: smartphone
   Similarity: 0.8523

2. Samsung Galaxy S24 Ultra 512GB
   Price: 27990000₫
   Category: smartphone
   Similarity: 0.7234

3. MacBook Pro 14 inch M3
   Price: 41990000₫
   Category: laptop
   Similarity: 0.4162
```

---

### 3.4 Exercise 3: UPDATE Documents (15 min)

**Location:** `exercise_3_update_documents()` function

**Goal:** Update metadata for existing documents (e.g., price changes).

**Implementation Steps:**

**Step 1:** Get collection
```python
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_collection(name="products")
```

**Step 2:** Update document
```python
collection.update(
    ids=["1"],
    metadatas=[{
        "name": "iPhone 15 Pro Max 256GB",
        "price": "28990000",  # Price drop from 29990000!
        "category": "smartphone"
    }]
)

print("✓ Updated product id='1' with new price")
```

**Important notes:**
- `ids` is a list (even for one update)
- `metadatas` is a list of dictionaries
- Must provide **complete** metadata (ChromaDB replaces, not merges)
- Embeddings remain unchanged (only metadata updates)

**Step 3:** Verify update
```python
result = collection.get(ids=["1"])
print(f"\nUpdated metadata: {result['metadatas'][0]}")
```

---

### 3.5 Exercise 4: DELETE Documents (15 min)

**Location:** `exercise_4_delete_documents()` function

**Goal:** Remove documents from ChromaDB.

**Implementation Steps:**

**Step 1:** Get collection
```python
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_collection(name="products")
```

**Step 2:** Delete document
```python
collection.delete(ids=["3"])

print("✓ Deleted product id='3' (MacBook Pro 14 inch)")
```

**Step 3:** Verify deletion
```python
print(f"Documents after deletion: {collection.count()}")
```

**Expected output:**
```
======================================================================
EXERCISE 4: Delete Documents
======================================================================
Documents before deletion: 3
✓ Deleted product id='3' (MacBook Pro 14 inch)
Documents after deletion: 2
```

## Step 4: Verify Your Work (15 minutes)

### 4.1 Run the Verification Script

```bash
python solution/verify.py
```

### 4.2 Understand the Results

The verification script tests:

#### TEST 1: get_embedding()
- Returns a list
- Has 1536 dimensions
- Contains float values

#### TEST 2: ChromaDB Setup
- Creates persistent client
- Creates collection
- Inserts documents
- Counts documents correctly

#### TEST 3: Vector Search
- Queries collection
- Returns results
- Results have correct structure

#### TEST 4: Update and Delete
- Updates metadata correctly
- Deletes documents
- Count changes as expected

### 4.3 Interpreting Scores

**All tests passed (4/4):**
```
🎉 Congratulations! All tests passed!
You're ready for Lesson 4: Building Basic RAG Pipeline
```
→ You're ready for Lesson 4!

**Some tests failed:**
```
⚠ 2 test(s) failed. Keep working on the exercises!
```
→ Review the error messages and fix the issues

## Summary

Congratulations! You've mastered vector databases with ChromaDB. You can now:
- Store embeddings efficiently
- Search for similar documents fast
- Manage vector data with CRUD operations
- Understand how this enables RAG systems

**Key Takeaway:** ChromaDB bridges the gap between embeddings (Lesson 2) and RAG (Lesson 4) by providing fast, scalable similarity search.

**Next:** [Lesson 4: Building Basic RAG Pipeline](../lesson-04-basic-rag/README.md)

---

**Questions or issues?** Check [docs/troubleshooting.md](../../docs/troubleshooting.md) or review the solution code in `solution/chromadb_complete.py`.

**Completed successfully?** Great! You're ready to build a complete RAG system in Lesson 4!
