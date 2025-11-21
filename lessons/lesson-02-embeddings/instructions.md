# Lesson 2: Understanding Embeddings - Step-by-Step Instructions

## Introduction

Welcome to Lesson 2! In this lesson, you'll learn about embeddings - the fundamental technology that powers semantic search in RAG systems. By the end, you'll understand how text is converted to numerical vectors and how to use those vectors to find similar content.

## What You'll Build

You'll implement three core functions that are used in the reference RAG solution:
1. `get_embedding()` - Generate embeddings using OpenAI's API
2. `cosine_similarity()` - Calculate how similar two pieces of text are
3. `normalize_embedding()` - Prepare vectors for accurate comparison

## Step 1: Setup and Preparation (5 minutes)

### 1.1 Navigate to Lesson Directory

```bash
cd lessons/lesson-02-embeddings
```

### 1.2 Verify Environment

Make sure your virtual environment is activated and dependencies are installed:

```bash
# Activate virtual environment (if not already active)
# On Windows:
# .venv\Scripts\activate  (or venv\Scripts\activate)
# On Mac/Linux:
# source .venv/bin/activate  (or source venv/bin/activate)

# Verify packages
python -c "import openai; import numpy; print('✓ Packages ready')"

# If packages not installed, use uv (fast!):
# uv pip install openai numpy python-dotenv
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

Before writing code, let's see embeddings in action.

### 2.1 Run the Demo Script

```bash
python solution/embeddings_demo.py
```

**What to observe:**

1. **Demonstration 1: Basic Embeddings**
   - See how text becomes a 1536-dimensional vector
   - Notice the vector contains float values (positive and negative)
   - Each dimension captures some aspect of meaning

2. **Demonstration 2: Product Similarity**
   - Query: "Tôi muốn mua iPhone 15 Pro" (Vietnamese)
   - Notice iPhone products rank highest, even with Vietnamese query
   - This is semantic search in action!

3. **Demonstration 3: Normalization**
   - Before normalization: magnitude varies
   - After normalization: magnitude = 1.0
   - This ensures fair comparison in vector search

4. **Demonstration 4: Real Product Search**
   - See how embeddings work with actual product data
   - Multiple queries, different languages, all work!

### 2.2 Key Takeaways

After running the demo, you should understand:
- ✅ Embeddings convert text → numbers
- ✅ Similar meanings → similar vectors
- ✅ Cosine similarity measures similarity
- ✅ Normalization is critical for accuracy
- ✅ Works across languages (Vietnamese, English)

## Step 3: Implement Core Functions (45 minutes)

Now it's your turn! Open `exercises/my_embeddings.py` in your code editor.

### 3.1 Implement `get_embedding()`

**Location:** Line ~35 in `exercises/my_embeddings.py`

**Task:** Generate an embedding vector for the given text.

**Hints:**
```python
def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    # STEP 1: Call the API
    response = client.embeddings.create(
        input=text,
        model=model
    )

    # STEP 2: Extract the embedding from response
    return response.data[0].embedding
```

**How to test:**
```python
# Add this at the bottom of the file temporarily
if __name__ == "__main__":
    embedding = get_embedding("test")
    print(f"Dimension: {len(embedding)}")  # Should be 1536
    print(f"Sample: {embedding[:5]}")      # Should show 5 floats
```

**Expected output:**
```
Dimension: 1536
Sample: [0.023, -0.015, 0.041, -0.008, 0.019]
```

### 3.2 Implement `cosine_similarity()`

**Location:** Line ~50 in `exercises/my_embeddings.py`

**Task:** Calculate cosine similarity between two vectors.

**Formula:**
```
cos(θ) = (A · B) / (||A|| × ||B||)
```

**Implementation Steps:**
```python
def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    # STEP 1: Convert to numpy arrays
    a = np.array(vec1)
    b = np.array(vec2)

    # STEP 2: Calculate dot product
    dot_product = np.dot(a, b)

    # STEP 3: Calculate magnitudes (L2 norms)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    # STEP 4: Calculate cosine similarity
    similarity = dot_product / (norm_a * norm_b)

    return float(similarity)
```

**How to test:**
```python
# Test with known vectors
vec1 = [1.0, 0.0, 0.0]
vec2 = [1.0, 0.0, 0.0]
vec3 = [0.0, 1.0, 0.0]

print(cosine_similarity(vec1, vec2))  # Should be 1.0 (identical)
print(cosine_similarity(vec1, vec3))  # Should be 0.0 (orthogonal)
```

**Expected results:**
- Identical vectors: 1.0
- Orthogonal vectors: 0.0
- Similar vectors: 0.7 - 0.9
- Different vectors: 0.0 - 0.3

### 3.3 Implement `normalize_embedding()`

**Location:** Line ~70 in `exercises/my_embeddings.py`

**Task:** Normalize a vector to unit length (magnitude = 1.0).

**Why this matters:** The reference RAG solution uses this to ensure accurate similarity calculations.

**Implementation:**
```python
def normalize_embedding(embedding: List[float]) -> np.ndarray:
    # STEP 1: Convert to numpy array
    embedding_array = np.array(embedding)

    # STEP 2: Calculate magnitude (L2 norm)
    norm = np.linalg.norm(embedding_array)

    # STEP 3: Divide by magnitude
    normalized = embedding_array / norm

    return normalized
```

**How to test:**
```python
embedding = get_embedding("test text")
print(f"Before: {np.linalg.norm(embedding)}")  # Some value

normalized = normalize_embedding(embedding)
print(f"After: {np.linalg.norm(normalized)}")   # Should be 1.0
```

**Expected output:**
```
Before: 4.732891
After: 1.0
```

## Step 4: Complete the Exercises (45 minutes)

Now that you have the core functions, complete the exercises in `exercises/my_embeddings.py`.

### Exercise 1: Generate Embeddings (10 min)

**Goal:** Generate embeddings for product descriptions and inspect them.

**Instructions:**
1. Uncomment the TODO code in `exercise_1_generate_embeddings()`
2. Use your `get_embedding()` function
3. Print the dimension and sample values

**Solution approach:**
```python
embeddings = []
for product in products:
    embedding = get_embedding(product)
    embeddings.append(embedding)
    print(f"\nProduct: {product}")
    print(f"  Dimension: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
```

### Exercise 2: Calculate Similarity (15 min)

**Goal:** Find which product is most similar to a Vietnamese query.

**Instructions:**
1. Generate query embedding
2. Generate embeddings for each product
3. Calculate similarity scores
4. Identify the most similar product

**Solution approach:**
```python
query_embedding = get_embedding(query)

for product in products:
    product_embedding = get_embedding(product)
    similarity = cosine_similarity(query_embedding, product_embedding)
    print(f"{product}: {similarity:.4f}")
```

**Expected:** iPhone should have the highest score (~0.75-0.85)

### Exercise 3: Normalization (10 min)

**Goal:** Verify that normalization works correctly.

**Instructions:**
1. Generate an embedding
2. Calculate its magnitude
3. Normalize it
4. Verify normalized magnitude = 1.0

**Solution approach:**
```python
embedding = get_embedding(text)
magnitude_before = np.linalg.norm(embedding)

normalized = normalize_embedding(embedding)
magnitude_after = np.linalg.norm(normalized)

is_normalized = abs(magnitude_after - 1.0) < 0.0001
print(f"Properly normalized: {is_normalized}")
```

### Exercise 4: Find Most Similar Product (10 min)

**Goal:** Build a similarity search function.

**Instructions:**
1. Normalize query embedding
2. For each product, normalize and calculate similarity
3. Find the product with highest similarity

**Solution approach:**
```python
query_normalized = normalize_embedding(get_embedding(query))

results = []
for product in products:
    product_emb = get_embedding(product)
    product_normalized = normalize_embedding(product_emb)
    similarity = cosine_similarity(query_normalized, product_normalized)
    results.append((product, similarity))

# Sort by similarity
results.sort(key=lambda x: x[1], reverse=True)
print(f"Most similar: {results[0][0]} (score: {results[0][1]:.4f})")
```

### Bonus Exercise: Multilingual (Optional)

Test how embeddings handle multiple languages!

## Step 5: Verify Your Work (15 minutes)

### 5.1 Run the Verification Script

```bash
python solution/verify.py
```

### 5.2 Understand the Results

The verification script tests:

1. **✅ TEST 1: get_embedding()**
   - Returns a list
   - Has 1536 dimensions
   - Contains float values

2. **✅ TEST 2: cosine_similarity()**
   - Identical vectors → 1.0
   - Orthogonal vectors → 0.0
   - Correctly ranks similar vs different

3. **✅ TEST 3: normalize_embedding()**
   - Returns numpy array
   - Magnitude = 1.0 after normalization

4. **✅ TEST 4: Exercise completion**
   - Checks if you removed TODO comments
   - Verifies functions are implemented

### 5.3 Interpreting Scores

**All tests passed (4/4):**
```
🎉 Congratulations! All tests passed!
```
→ You're ready for Lesson 3!

**Some tests failed:**
```
⚠ 2 test(s) failed. Keep working on the exercises!
```
→ Review the error messages and fix the issues

### 5.4 Common Issues and Fixes

**Issue:** "Function not implemented (still has 'pass')"
```python
# Bad:
def get_embedding(text: str):
    pass  # ← Remove this!

# Good:
def get_embedding(text: str):
    response = client.embeddings.create(...)
    return response.data[0].embedding
```

**Issue:** "Expected 1536 dimensions, got XXX"
- Make sure you're using `text-embedding-3-small` model
- Check that you're extracting `response.data[0].embedding`

**Issue:** "Similarity should be between -1 and 1"
- Verify your cosine similarity formula
- Check that you're dividing by the product of norms

**Issue:** "Normalized magnitude should be 1.0"
- Make sure you're dividing by `np.linalg.norm()`
- Check that you're returning the normalized vector, not the norm itself

## Step 6: Understanding the Connection to RAG (10 minutes)

### 6.1 Review the Reference Solution

Open `final-project/reference-solution/rag.py` and look at lines 17-23:

```python
def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
```

**This is exactly what you just implemented!**

Now look at lines 26-56 to see how it's used in the RAG tool:

```python
@function_tool
def rag(query: str) -> str:
    # 1. Get query embedding
    query_embedding = get_embedding(query)

    # 2. Normalize (what you learned!)
    query_embedding = query_embedding / np.linalg.norm(query_embedding)

    # 3. Search ChromaDB (next lesson!)
    search_results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    # 4. Return results
    return search_result
```

### 6.2 The Big Picture

```
User Query: "Tôi muốn mua iPhone"
    ↓
[get_embedding] → [0.023, -0.015, ..., 0.008]
    ↓
[normalize] → [0.0048, -0.0031, ..., 0.0017]
    ↓
[ChromaDB search] → Find 3 most similar products
    ↓
[Return to AI agent] → Agent answers using real product data
```

You've just mastered the first two steps!

## Step 7: Reflection and Next Steps (5 minutes)

### What You've Learned

✅ How to generate embeddings using OpenAI's API
✅ How to calculate semantic similarity
✅ Why normalization is critical
✅ How embeddings enable cross-lingual search
✅ How these fit into the RAG system

### Key Insights

💡 **Insight 1:** Embeddings capture meaning, not just keywords
- "iPhone" and "điện thoại iPhone" have high similarity
- Semantic search > keyword matching

💡 **Insight 2:** Normalization ensures fair comparison
- All vectors become unit length (magnitude = 1.0)
- Prevents longer vectors from dominating similarity scores

💡 **Insight 3:** Cosine similarity is efficient
- Only need dot product and norms
- Fast enough for thousands of comparisons

### Prepare for Lesson 3

In the next lesson, you'll learn about **ChromaDB** - a vector database that:
- Stores millions of embeddings efficiently
- Performs fast similarity search
- Persists data across restarts

This completes the RAG pipeline:
1. ✅ **Lesson 2:** Generate embeddings
2. → **Lesson 3:** Store in vector database
3. → **Lesson 4:** Build RAG pipeline
4. → **Lesson 5:** Add AI agents

## Troubleshooting

### "Module 'openai' has no attribute 'embeddings'"

You might be using an older version of the OpenAI library. Update it:
```bash
# Using uv (faster):
uv pip install --upgrade openai

# Or using pip:
pip install --upgrade openai
```

### "Rate limit exceeded"

You're making too many API calls. Solutions:
1. Wait 60 seconds and try again
2. Reduce the number of examples in exercises
3. Check your OpenAI account has credits

### "API key not found"

Make sure:
1. `.env` file exists in project root (not in lesson directory)
2. File contains: `OPENAI_API_KEY=sk-...`
3. No extra spaces or quotes around the key
4. You're running from correct directory

### Embeddings look wrong

Check:
```python
embedding = get_embedding("test")
print(f"Type: {type(embedding)}")        # Should be: list
print(f"Length: {len(embedding)}")       # Should be: 1536
print(f"Sample: {embedding[:3]}")        # Should be floats
print(f"All floats: {all(isinstance(x, float) for x in embedding)}")  # Should be: True
```

## Additional Practice (Optional)

Want more practice? Try these extensions:

1. **Compare embedding models:**
   - Try `text-embedding-3-large` (3072 dimensions)
   - Compare speed and similarity scores

2. **Build a product recommender:**
   - Load products from CSV
   - User selects a product
   - Find 5 most similar products

3. **Multilingual testing:**
   - Same query in 5 languages
   - Compare similarity scores
   - Which language pairs work best?

4. **Visualization:**
   - Use PCA or t-SNE to reduce embeddings to 2D
   - Plot products on a chart
   - See clusters of similar products

## Summary

Congratulations! You've completed Lesson 2 and learned the foundation of semantic search. You can now:
- Generate embeddings for any text
- Calculate how similar two texts are
- Normalize vectors for accurate comparison
- Understand how embeddings power RAG systems

**Next:** [Lesson 3: Vector Databases (ChromaDB)](../lesson-03-vector-database/README.md)

---

**Questions or issues?** Check `docs/troubleshooting.md` or review the solution code in `solution/embeddings_demo.py`.

**Completed successfully?** Great! Move on to Lesson 3 where you'll learn to store and search millions of embeddings efficiently with ChromaDB.
