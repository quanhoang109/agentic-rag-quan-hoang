"""
Lesson 2: Understanding Embeddings
Demonstrates how text embeddings work using real mobile phone product data
Based on the reference solution in final-project/reference-solution/rag.py
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
from typing import List

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate an embedding vector for the given text using OpenAI's API.
    This is the same function used in the reference RAG solution.

    Args:
        text: The input text to embed
        model: The OpenAI embedding model (default: text-embedding-3-small)

    Returns:
        A list of 1536 floats representing the embedding vector
    """
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Formula: cos(θ) = (A · B) / (||A|| × ||B||)
    Range: -1 to 1, where:
      - 1.0 means vectors are identical
      - 0.0 means vectors are orthogonal (unrelated)
      - -1.0 means vectors are opposite

    Args:
        vec1: First embedding vector
        vec2: Second embedding vector

    Returns:
        Cosine similarity score between -1 and 1
    """
    a = np.array(vec1)
    b = np.array(vec2)

    # Calculate cosine similarity
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    similarity = dot_product / (norm_a * norm_b)
    return float(similarity)


def normalize_embedding(embedding: List[float]) -> np.ndarray:
    """
    Normalize an embedding vector to unit length.
    This is critical for accurate cosine similarity in vector databases.

    From reference solution: query_embedding = query_embedding / np.linalg.norm(query_embedding)

    Args:
        embedding: The embedding vector to normalize

    Returns:
        Normalized embedding as numpy array with magnitude = 1.0
    """
    embedding_array = np.array(embedding)
    norm = np.linalg.norm(embedding_array)
    return embedding_array / norm


def demonstrate_basic_embeddings():
    """
    Demonstrates how to generate embeddings and their basic properties.
    """
    print("=" * 70)
    print("DEMONSTRATION 1: Generating Embeddings")
    print("=" * 70)

    text = "iPhone 15 Pro Max 256GB"
    print(f"\nInput text: '{text}'")
    print("\nCalling OpenAI API to generate embedding...")

    embedding = get_embedding(text)
    embedding_array = np.array(embedding)

    print(f"\n✓ Embedding generated successfully!")
    print(f"  Dimensions: {len(embedding)}")
    print(f"  Model: text-embedding-3-small")
    print(f"\nFirst 10 values: {embedding[:10]}")
    print(f"\nVector properties:")
    print(f"  Min value: {np.min(embedding_array):.6f}")
    print(f"  Max value: {np.max(embedding_array):.6f}")
    print(f"  Mean: {np.mean(embedding_array):.6f}")
    print(f"  Magnitude (L2 norm): {np.linalg.norm(embedding_array):.6f}")


def demonstrate_product_similarity():
    """
    Demonstrates semantic similarity using real product queries.
    Shows how similar products have higher similarity scores.
    """
    print("\n\n" + "=" * 70)
    print("DEMONSTRATION 2: Product Similarity Search")
    print("=" * 70)

    # Simulate product database entries
    products = {
        "iphone_15": "iPhone 15 Pro Max 256GB - Titanium Blue",
        "iphone_14": "iPhone 14 Pro 128GB - Space Black",
        "samsung": "Samsung Galaxy S24 Ultra 512GB",
        "laptop": "MacBook Pro 14 inch M3 chip"
    }

    # User query
    query = "Tôi muốn mua iPhone 15 Pro"

    print(f"\nUser query: '{query}'")
    print("\nProducts in database:")
    for i, (key, product) in enumerate(products.items(), 1):
        print(f"  {i}. {product}")

    print("\nGenerating embeddings...")
    query_embedding = get_embedding(query)
    product_embeddings = {key: get_embedding(text) for key, text in products.items()}

    print("\n" + "=" * 70)
    print("SIMILARITY SCORES (Higher = More Relevant)")
    print("=" * 70)

    # Calculate similarities
    similarities = []
    for key, product in products.items():
        similarity = cosine_similarity(query_embedding, product_embeddings[key])
        similarities.append((product, similarity))

    # Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)

    print(f"\nRanked results for: '{query}'\n")
    for rank, (product, score) in enumerate(similarities, 1):
        bar = "█" * int(score * 50)
        print(f"{rank}. {product}")
        print(f"   Score: {score:.4f} {bar}")
        print()

    print("✓ Notice: iPhone products rank highest, even though query is in Vietnamese!")


def demonstrate_normalization():
    """
    Demonstrates why normalization is important for vector search.
    Shows the difference between normalized and non-normalized similarity.
    """
    print("\n\n" + "=" * 70)
    print("DEMONSTRATION 3: Vector Normalization (Critical for RAG)")
    print("=" * 70)

    query = "điện thoại giá rẻ"
    product = "Samsung Galaxy A14 - Giá tốt nhất"

    print(f"\nQuery: '{query}'")
    print(f"Product: '{product}'")

    query_emb = get_embedding(query)
    product_emb = get_embedding(product)

    # Without normalization
    similarity_raw = cosine_similarity(query_emb, product_emb)

    # With normalization (as done in reference solution)
    query_normalized = normalize_embedding(query_emb)
    product_normalized = normalize_embedding(product_emb)
    similarity_normalized = cosine_similarity(query_normalized, product_normalized)

    print(f"\nOriginal magnitude:")
    print(f"  Query vector: {np.linalg.norm(query_emb):.6f}")
    print(f"  Product vector: {np.linalg.norm(product_emb):.6f}")

    print(f"\nAfter normalization:")
    print(f"  Query vector: {np.linalg.norm(query_normalized):.6f}")
    print(f"  Product vector: {np.linalg.norm(product_normalized):.6f}")

    print(f"\nSimilarity scores:")
    print(f"  Without normalization: {similarity_raw:.6f}")
    print(f"  With normalization: {similarity_normalized:.6f}")

    print(f"\n✓ Normalization ensures consistent comparison!")
    print(f"  Reference solution code: query_embedding / np.linalg.norm(query_embedding)")


def demonstrate_real_product_search():
    """
    Demonstrates semantic search on actual product data from hoanghamobile.csv
    """
    print("\n\n" + "=" * 70)
    print("DEMONSTRATION 4: Real Product Data Search")
    print("=" * 70)

    # Load sample products from CSV
    csv_path = "../../../data/hoanghamobile.csv"
    if not os.path.exists(csv_path):
        print("\n⚠ Note: Product CSV not found. Using sample data instead.")
        sample_products = [
            "iPhone 15 Pro Max 256GB - Titanium Natural - 29.990.000₫",
            "Samsung Galaxy S24 Ultra 256GB - Titanium Gray - 26.990.000₫",
            "OPPO Find N3 Flip 5G 256GB - 19.990.000₫",
            "Xiaomi 14 Ultra 16GB/512GB - 24.990.000₫",
            "Nokia 3210 4G - 1.490.000₫"
        ]
    else:
        try:
            df = pd.read_csv(csv_path, nrows=100)
            sample_products = []
            for _, row in df.head(5).iterrows():
                title = row['title'] if 'title' in row else "Unknown"
                price = row['current_price'] if 'current_price' in row else ""
                sample_products.append(f"{title} - {price}")
        except Exception as e:
            print(f"\n⚠ Could not load CSV: {e}. Using sample data.")
            sample_products = [
                "iPhone 15 Pro Max 256GB - 29.990.000₫",
                "Samsung Galaxy S24 Ultra - 26.990.000₫",
                "OPPO Find N3 Flip 5G - 19.990.000₫"
            ]

    queries = [
        "Tôi cần điện thoại cao cấp nhất",
        "flagship phone under 30 million",
        "smartphone giá rẻ dưới 2 triệu"
    ]

    print("\nProduct database (sample):")
    for i, product in enumerate(sample_products, 1):
        print(f"  {i}. {product}")

    # Generate product embeddings once
    print("\nGenerating product embeddings...")
    product_embeddings = [get_embedding(p) for p in sample_products]

    for query in queries:
        print("\n" + "=" * 70)
        print(f"Query: '{query}'")
        print("=" * 70)

        query_embedding = get_embedding(query)
        query_normalized = normalize_embedding(query_embedding)

        # Find top matches
        results = []
        for i, product in enumerate(sample_products):
            product_normalized = normalize_embedding(product_embeddings[i])
            similarity = cosine_similarity(query_normalized, product_normalized)
            results.append((product, similarity))

        # Sort and display top 3
        results.sort(key=lambda x: x[1], reverse=True)
        print("\nTop 3 matches:")
        for rank, (product, score) in enumerate(results[:3], 1):
            print(f"  {rank}. {product}")
            print(f"     Similarity: {score:.4f}")


def main():
    """
    Run all demonstrations to understand embeddings in RAG context.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "LESSON 2: UNDERSTANDING EMBEDDINGS" + " " * 19 + "║")
    print("║" + " " * 18 + "Mobile Phone Shop RAG System" + " " * 22 + "║")
    print("╚" + "=" * 68 + "╝")

    try:
        # Run demonstrations
        demonstrate_basic_embeddings()
        demonstrate_product_similarity()
        demonstrate_normalization()
        demonstrate_real_product_search()

        print("\n\n" + "=" * 70)
        print("KEY TAKEAWAYS")
        print("=" * 70)
        print("""
1. Embeddings convert text → numerical vectors (1536 dimensions)
2. Similar meanings → similar vectors (high cosine similarity)
3. Cosine similarity ranges from -1 to 1 (higher = more similar)
4. Normalization is CRITICAL for accurate vector search
   - Reference: query_embedding / np.linalg.norm(query_embedding)
5. Semantic search works across languages (Vietnamese ↔ English)
6. These embeddings power the RAG system's product search
7. Next lesson: Store embeddings in ChromaDB for efficient retrieval
        """)

        print("=" * 70)
        print("✅ All demonstrations completed successfully!")
        print("=" * 70)
        print("\nNext: Lesson 3 - Vector Databases (ChromaDB)")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Check OPENAI_API_KEY in .env file")
        print("  2. Ensure you have API credits")
        print("  3. Check internet connection")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
