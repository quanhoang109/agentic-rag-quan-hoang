"""
Setup Script: Load sample products into ChromaDB
This script loads data from sample_products.json and inserts it into ChromaDB.

Run: python solution/setup_sample_data.py
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


def main():
    """Load sample products into ChromaDB."""
    print("\n" + "=" * 70)
    print("SETUP: Loading Sample Products into ChromaDB")
    print("=" * 70)

    # Step 1: Load products from JSON
    print("\n1. Loading products from sample_products.json...")
    json_path = os.path.join(os.path.dirname(__file__), "sample_products.json")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
        print(f"   ✓ Loaded {len(products)} products")
    except FileNotFoundError:
        print(f"   ❌ Error: sample_products.json not found at {json_path}")
        return 1

    # Step 2: Create ChromaDB client and collection
    print("\n2. Setting up ChromaDB...")
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_or_create_collection(name="sample_products")
    print(f"   ✓ Collection '{collection.name}' ready")

    # Step 3: Prepare data for batch insert
    print("\n3. Generating embeddings...")
    ids = []
    embeddings = []
    metadatas = []

    for product in products:
        # Create rich searchable text
        text = f"{product['name']} {product['description']}"

        # Generate embedding
        embedding = get_embedding(text)

        # Prepare data
        ids.append(product['id'])
        embeddings.append(embedding)
        metadatas.append({
            "name": product['name'],
            "price": product['price'],
            "category": product['category'],
            "brand": product['brand'],
            "description": product['description']
        })

        print(f"   ✓ {product['name']}")

    # Step 4: Batch insert
    print("\n4. Inserting into ChromaDB...")
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"   ✓ Inserted {len(ids)} products")

    # Step 5: Verify
    print("\n5. Verification:")
    print(f"   Total documents in collection: {collection.count()}")

    # Test search
    query = "tai nghe"
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    print(f"\n   Test query: '{query}'")
    print("   Top 3 results:")
    for i, metadata in enumerate(results['metadatas'][0], 1):
        print(f"     {i}. {metadata['name']} - {int(metadata['price']):,}₫")

    print("\n" + "=" * 70)
    print("✓ Setup completed successfully!")
    print("=" * 70)
    print("\nYou can now:")
    print("  - Run queries against the 'sample_products' collection")
    print("  - Experiment with different search queries")
    print("  - Practice with metadata filtering")
    print("\n")

    return 0


if __name__ == "__main__":
    exit(main())
