"""
Lesson 3: ChromaDB Demonstrations
This file demonstrates ChromaDB features before students do the exercises.

Run: python solution/chromadb_demo.py
"""

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI API."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding


def demo_1_basic_setup():
    """Demonstration 1: Basic ChromaDB Setup"""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 1: Basic ChromaDB Setup")
    print("=" * 70)

    print("\n1. Creating Persistent Client:")
    print("   chroma_client = chromadb.PersistentClient(path='db')")
    chroma_client = chromadb.PersistentClient(path="db")
    print("   ✓ Client created - data will be saved to 'db/' directory")

    print("\n2. Creating Collection:")
    print("   collection = chroma_client.get_or_create_collection('demo')")
    collection = chroma_client.get_or_create_collection(name="demo")
    print(f"   ✓ Collection created: '{collection.name}'")

    print("\n3. Inserting Sample Documents:")
    products = [
        "iPhone 15 Pro Max - Camera 48MP",
        "Samsung Galaxy S24 - Camera 200MP",
        "MacBook Pro M3 - Chip Apple Silicon"
    ]

    ids = ["demo_1", "demo_2", "demo_3"]
    embeddings = [get_embedding(p) for p in products]
    metadatas = [{"product": p} for p in products]

    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
    print(f"   ✓ Inserted {len(products)} documents")
    print(f"   Total documents in collection: {collection.count()}")

    print("\n4. Document Structure:")
    print("   - IDs: Unique identifiers ['demo_1', 'demo_2', 'demo_3']")
    print("   - Embeddings: 1536-dimensional vectors")
    print("   - Metadata: Additional information (product names)")


def demo_2_vector_search():
    """Demonstration 2: Vector Similarity Search"""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 2: Vector Similarity Search")
    print("=" * 70)

    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="demo")

    query = "Tôi muốn mua điện thoại với camera tốt"
    print(f"\nQuery: '{query}'")

    print("\n1. Generate Query Embedding:")
    query_embedding = get_embedding(query)
    print(f"   ✓ Generated embedding (dimension: {len(query_embedding)})")

    print("\n2. Search ChromaDB:")
    print("   results = collection.query(query_embeddings=[...], n_results=3)")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    print("\n3. Results (ranked by similarity):")
    for i, (metadata, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0]), 1):
        similarity = 1 - distance
        print(f"   {i}. {metadata['product']}")
        print(f"      Distance: {distance:.4f} | Similarity: {similarity:.4f}")

    print("\n4. Understanding Results:")
    print("   - Lower distance = Higher similarity")
    print("   - ChromaDB uses HNSW algorithm for fast search")
    print("   - Semantic search: Understands 'điện thoại camera tốt' → phones with good cameras")


def demo_3_metadata_filtering():
    """Demonstration 3: Metadata Filtering"""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 3: Metadata Filtering")
    print("=" * 70)

    chroma_client = chromadb.PersistentClient(path="db")

    # Create new collection with more detailed metadata
    collection = chroma_client.get_or_create_collection(name="demo_filtered")

    print("\n1. Inserting Products with Rich Metadata:")
    products_data = [
        {"name": "iPhone 15 Pro", "category": "smartphone", "price": 25000000},
        {"name": "Samsung S24", "category": "smartphone", "price": 20000000},
        {"name": "MacBook Pro", "category": "laptop", "price": 40000000},
        {"name": "iPad Pro", "category": "tablet", "price": 22000000},
    ]

    ids = [f"filter_{i}" for i in range(len(products_data))]
    embeddings = [get_embedding(p["name"]) for p in products_data]
    metadatas = [{"name": p["name"], "category": p["category"], "price": p["price"]}
                 for p in products_data]

    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
    print(f"   ✓ Inserted {len(products_data)} products")

    print("\n2. Search with Metadata Filter (smartphones only):")
    query_embedding = get_embedding("sản phẩm di động")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"category": "smartphone"}  # Filter by category
    )

    print("   Results (filtered to smartphones):")
    for metadata in results['metadatas'][0]:
        print(f"   - {metadata['name']} ({metadata['category']})")

    print("\n3. Complex Filter (price < 25M):")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"price": {"$lt": 25000000}}  # Price less than 25M (numeric comparison)
    )

    print("   Results (price < 25M):")
    for metadata in results['metadatas'][0]:
        print(f"   - {metadata['name']}: {metadata['price']:,}₫")

    print("\n4. Available Filter Operators:")
    print("   - $eq: Equals")
    print("   - $ne: Not equals")
    print("   - $gt, $gte: Greater than (or equal)")
    print("   - $lt, $lte: Less than (or equal)")
    print("   - $and, $or: Logical operators")


def demo_4_distance_metrics():
    """Demonstration 4: Distance Metrics"""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 4: Distance Metrics")
    print("=" * 70)

    chroma_client = chromadb.PersistentClient(path="db")

    print("\n1. Cosine Distance (default):")
    print("   - Measures angle between vectors")
    print("   - Range: 0 (identical) to 2 (opposite)")
    print("   - Best for text embeddings")

    collection_cosine = chroma_client.get_or_create_collection(
        name="demo_cosine",
        metadata={"hnsw:space": "cosine"}
    )

    print("\n2. L2 Distance (Euclidean):")
    print("   - Measures straight-line distance")
    print("   - Range: 0 (identical) to ∞")
    print("   - Use when magnitude matters")

    collection_l2 = chroma_client.get_or_create_collection(
        name="demo_l2",
        metadata={"hnsw:space": "l2"}
    )

    print("\n3. Inner Product:")
    print("   - Dot product of vectors")
    print("   - Higher = more similar")
    print("   - Use with normalized embeddings")

    collection_ip = chroma_client.get_or_create_collection(
        name="demo_ip",
        metadata={"hnsw:space": "ip"}
    )

    print("\n4. Recommendation:")
    print("   ✓ Use COSINE for text embeddings (OpenAI, sentence transformers)")
    print("   ✓ It's the default and works best for semantic search")


def demo_5_batch_operations():
    """Demonstration 5: Batch Operations"""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 5: Batch Operations & Performance")
    print("=" * 70)

    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_or_create_collection(name="demo_batch")

    print("\n1. Loading Sample Data:")
    # Load sample products from JSON
    json_path = os.path.join(os.path.dirname(__file__), "sample_products.json")
    with open(json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    print(f"   ✓ Loaded {len(products)} products from JSON")

    print("\n2. Batch Insert (much faster than loop):")
    ids = [p["id"] for p in products]
    embeddings = [get_embedding(f"{p['name']} {p['description']}") for p in products]
    metadatas = [
        {
            "name": p["name"],
            "price": p["price"],
            "category": p["category"],
            "brand": p["brand"]
        }
        for p in products
    ]

    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
    print(f"   ✓ Inserted {len(products)} products in batch")

    print("\n3. Performance Comparison:")
    print("   - One-by-one: 100 products in ~10 seconds")
    print("   - Batch insert: 100 products in ~1 second (10x faster!)")

    print("\n4. Search Example:")
    query = "tai nghe chống ồn"
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    print(f"\n   Query: '{query}'")
    print("   Top results:")
    for i, metadata in enumerate(results['metadatas'][0], 1):
        print(f"   {i}. {metadata['name']} - {int(metadata['price']):,}₫")

    print("\n5. Connection to RAG Pipeline:")
    print("   ┌─────────────────┐")
    print("   │  User Query     │")
    print("   └────────┬────────┘")
    print("            ↓")
    print("   ┌─────────────────┐")
    print("   │  Get Embedding  │ ← Lesson 2")
    print("   └────────┬────────┘")
    print("            ↓")
    print("   ┌─────────────────┐")
    print("   │  ChromaDB Query │ ← Lesson 3 (YOU ARE HERE!)")
    print("   └────────┬────────┘")
    print("            ↓")
    print("   ┌─────────────────┐")
    print("   │  Retrieved Docs │")
    print("   └────────┬────────┘")
    print("            ↓")
    print("   ┌─────────────────┐")
    print("   │  LLM + Context  │ ← Lesson 4 (Next!)")
    print("   └────────┬────────┘")
    print("            ↓")
    print("   ┌─────────────────┐")
    print("   │  Final Response │")
    print("   └─────────────────┘")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "LESSON 3: ChromaDB DEMONSTRATIONS" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\nWatch these demonstrations before doing the exercises.\n")

    try:
        demo_1_basic_setup()
        demo_2_vector_search()
        demo_3_metadata_filtering()
        demo_4_distance_metrics()
        demo_5_batch_operations()

        print("\n" + "=" * 70)
        print("All demonstrations completed!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  1. ChromaDB provides fast, persistent vector search")
        print("  2. Use get_or_create_collection() to avoid errors")
        print("  3. Metadata filtering narrows results efficiently")
        print("  4. Batch operations are 10x faster than loops")
        print("  5. Cosine distance is best for text embeddings")
        print("\nNow try the exercises in exercises/my_chromadb.py!")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. OPENAI_API_KEY is set in .env file")
        print("  2. ChromaDB is installed (uv sync --no-install-project)")
        print("  3. sample_products.json exists in solution/ directory")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
