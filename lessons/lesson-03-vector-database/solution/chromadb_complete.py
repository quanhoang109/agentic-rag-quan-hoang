"""
Lesson 3: Complete Solution - Vector Database with ChromaDB
This file contains the complete, working solutions for all exercises.

Reference implementation demonstrating best practices.
"""

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate embedding using OpenAI API (from Lesson 2).

    Args:
        text: The input text to embed
        model: The OpenAI embedding model to use

    Returns:
        A list of floats representing the embedding vector
    """
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def exercise_1_insert_documents():
    """
    Exercise 1: Insert documents into ChromaDB

    Solution demonstrates:
    - Creating persistent ChromaDB client
    - Getting or creating collection
    - Generating embeddings
    - Batch inserting documents
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

    print("\nProducts to insert:")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product['name']} - {product['price']}₫")

    # Step 1: Create persistent client
    # Data will be saved to 'db/' directory
    chroma_client = chromadb.PersistentClient(path="db")

    # Step 2: Get or create collection
    # Uses get_or_create to avoid errors if collection already exists
    collection = chroma_client.get_or_create_collection(name="products")

    # Step 3: Generate embeddings for each product
    ids = []
    embeddings = []
    metadatas = []

    for product in products:
        # Create searchable text combining all product information
        text = f"{product['name']} có giá {product['price']} thuộc danh mục {product['category']}"

        # Generate embedding
        embedding = get_embedding(text)

        # Prepare data for batch insert
        ids.append(product['id'])
        embeddings.append(embedding)
        metadatas.append({
            "name": product['name'],
            "price": product['price'],
            "category": product['category']
        })

    # Step 4: Batch insert documents
    # More efficient than inserting one-by-one
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"\n✓ Inserted {len(ids)} documents into collection '{collection.name}'")
    print(f"Total documents in collection: {collection.count()}")


def exercise_2_vector_search():
    """
    Exercise 2: Query ChromaDB for similar documents

    Solution demonstrates:
    - Getting existing collection
    - Generating query embedding
    - Performing vector similarity search
    - Processing and displaying results
    """
    print("\n" + "=" * 70)
    print("EXERCISE 2: Vector Search")
    print("=" * 70)

    query = "Tôi muốn mua điện thoại iPhone"

    # Step 1: Get collection
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="products")

    # Step 2: Generate query embedding
    query_embedding = get_embedding(query)

    # Step 3: Search for top 3 similar documents
    # Note: query_embeddings takes a LIST even for single query
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Step 4: Display results
    print(f"\nQuery: '{query}'")
    print("\nTop 3 results:")

    # Iterate through results
    # results['metadatas'][0] contains metadata for first query
    # results['distances'][0] contains distances for first query
    for i, (metadata, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0]), 1):
        # Convert distance to similarity (lower distance = higher similarity)
        similarity = 1 - distance

        print(f"\n{i}. {metadata['name']}")
        print(f"   Price: {metadata['price']}₫")
        print(f"   Category: {metadata['category']}")
        print(f"   Similarity: {similarity:.4f}")


def exercise_3_update_documents():
    """
    Exercise 3: Update existing documents

    Solution demonstrates:
    - Updating metadata for existing documents
    - Verifying updates
    - Best practices for metadata updates
    """
    print("\n" + "=" * 70)
    print("EXERCISE 3: Update Documents")
    print("=" * 70)

    # Step 1: Get collection
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="products")

    print(f"Current document count: {collection.count()}")

    # Step 2: Update document with id="1"
    # Important: Must provide COMPLETE metadata (ChromaDB replaces, not merges)
    collection.update(
        ids=["1"],
        metadatas=[{
            "name": "iPhone 15 Pro Max 256GB",
            "price": "28990000",  # Price drop from 29990000!
            "category": "smartphone"
        }]
    )

    print("\n✓ Updated product id='1' with new price (29990000 → 28990000)")

    # Step 3: Verify update
    result = collection.get(ids=["1"])
    updated_metadata = result['metadatas'][0]

    print(f"\nUpdated metadata:")
    print(f"  Name: {updated_metadata['name']}")
    print(f"  Price: {updated_metadata['price']}₫")
    print(f"  Category: {updated_metadata['category']}")


def exercise_4_delete_documents():
    """
    Exercise 4: Delete documents from collection

    Solution demonstrates:
    - Deleting documents by ID
    - Verifying deletion
    - Understanding when to delete
    """
    print("\n" + "=" * 70)
    print("EXERCISE 4: Delete Documents")
    print("=" * 70)

    # Step 1: Get collection
    chroma_client = chromadb.PersistentClient(path="db")
    collection = chroma_client.get_collection(name="products")

    print(f"Documents before deletion: {collection.count()}")

    # Step 2: Delete document with id="3" (MacBook)
    collection.delete(ids=["3"])

    print("\n✓ Deleted product id='3' (MacBook Pro 14 inch)")

    # Step 3: Verify deletion
    remaining_count = collection.count()
    print(f"Documents after deletion: {remaining_count}")

    # Verify the specific document is gone
    try:
        result = collection.get(ids=["3"])
        if len(result['ids']) == 0:
            print("✓ Document id='3' successfully removed")
    except Exception:
        print("✓ Document id='3' successfully removed")


def main():
    """Run all exercises in sequence."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "LESSON 3: COMPLETE SOLUTION" + " " * 26 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\nThis file demonstrates the complete, working solutions.\n")

    try:
        # Run all exercises
        exercise_1_insert_documents()
        exercise_2_vector_search()
        exercise_3_update_documents()
        exercise_4_delete_documents()

        print("\n" + "=" * 70)
        print("All exercises completed successfully!")
        print("=" * 70)
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. OPENAI_API_KEY is set in .env file")
        print("  2. ChromaDB dependencies are installed (uv sync --no-install-project)")
        print("  3. You have write permissions for the 'db' directory")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
