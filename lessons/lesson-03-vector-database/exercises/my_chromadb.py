"""
Lesson 3: Exercise - Vector Database with ChromaDB
Complete the TODOs below to practice working with ChromaDB

Student Name: _______________
Date: _______________
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
    TODO: Implement this function to generate embeddings using OpenAI API
    (Copy from Lesson 2)

    Steps:
    1. Use client.embeddings.create() with the text and model
    2. Extract and return the embedding vector from the response

    Hint: response.data[0].embedding

    Args:
        text: The input text to embed
        model: The OpenAI embedding model to use

    Returns:
        A list of floats representing the embedding vector
    """
    # TODO: Implement this function
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


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

    print("\nProducts to insert:")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product['name']} - {product['price']}₫")

    # TODO: Step 1 - Create persistent client
    # Hint: chromadb.PersistentClient(path="db")
    chroma_client = chromadb.PersistentClient(path="db")  # Fix this

    # TODO: Step 2 - Get or create collection
    # Hint: chroma_client.get_or_create_collection(name="products")
    collection = chroma_client.get_or_create_collection(name="products")  # Fix this

    # TODO: Step 3 - Generate embeddings for each product
    ids = []
    embeddings = []
    metadatas = []

    for product in products:
        # Create searchable text
        text = f"{product['name']} có giá {product['price']} thuộc danh mục {product['category']}"

        # TODO: Generate embedding
        # Hint: get_embedding(text)
        embedding = get_embedding(text)

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
    # Uncomment and complete:
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
    # Hint: chromadb.PersistentClient(path="db")
    chroma_client = chromadb.PersistentClient(path="db")  # Fix this
    # Hint: chroma_client.get_collection(name="products")
    collection = chroma_client.get_collection(name="products")  # Fix this

    # TODO: Step 2 - Generate query embedding
    # Hint: get_embedding(query)
    query_embedding = get_embedding(query)  # Fix this

    # TODO: Step 3 - Search for top 3 similar documents
    # Hint: collection.query(query_embeddings=[...], n_results=3)
    # Note: query_embeddings takes a LIST even for one query!
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
        )  

    # TODO: Step 4 - Display results
    print(f"\nQuery: '{query}'")
    print("\nTop 3 results:")
    for i, (meta, distance) in enumerate(zip(results['metadatas'][0], results['distances'][0]), 1):
        similarity = 1 - distance
        print(f"\n{i}. {meta['name']}")
        print(f"   Price: {meta['price']}₫")
        print(f"   Similarity: {similarity:.4f}")
        
    # Hint: Iterate through results['metadatas'][0] and results['distances'][0]
    # Remember: similarity = 1 - distance
    # for i, (metadata, distance) in enumerate(zip(...)):
    #     similarity = 1 - distance
    #     print(f"\n{i+1}. {metadata['name']}")
    #     print(f"   Price: {metadata['price']}₫")
    #     print(f"   Similarity: {similarity:.4f}")


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
    chroma_client = chromadb.PersistentClient(path='db')  # Fix this
    collection = chroma_client.get_collection(name="products")  # Fix this

    print(f"Current document count: {collection.count()}")

    # TODO: Step 2 - Update document with id="1"
    # Change price to "28990000" (price drop!)
    # Hint: 
    collection.update(
        ids=["1"],
        metadatas=[{
            "name": "iPhone 15 Pro Max 256GB",
            "price": "28990000",
            "category": "smartphone"
        }]
    )

    print("\n✓ Updated product id='1' with new price")

    # TODO: Step 3 - Query to verify
    # Hint: collection.get(ids=["1"])
    update_data = collection.get(ids=["1"])
    result = update_data['metadatas'][0]
    print(f"\nUpdated metadata: {result}")
    print(f"  Name: {result['name']}")
    print(f"  Price: {result['price']}₫")
    print(f"  Category: {result['category']}")


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

    print(f"Documents before deletion: {collection.count()}")

    # TODO: Step 2 - Delete document with id="3" (MacBook)
    # Hint: collection.delete(ids=["3"])

    print("\n✓ Deleted product id='3' (MacBook Pro 14 inch)")

    # TODO: Step 3 - Verify by counting remaining documents
    print(f"Documents after deletion: {collection.count()}")


def main():
    """
    Run all exercises.
    Uncomment exercises as you complete them.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "LESSON 3: EXERCISES" + " " * 29 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\nComplete the TODO items in each exercise function.")
    print("Uncomment the function calls below as you complete them.\n")

    try:
        # Uncomment as you complete each exercise
        exercise_1_insert_documents()
        exercise_2_vector_search()
        exercise_3_update_documents()
        # exercise_4_delete_documents()

        print("\n" + "=" * 70)
        print("Exercises completed! Run verify.py to check your solutions.")
        print("=" * 70)
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. OPENAI_API_KEY is set in .env file")
        print("  2. You've implemented the required functions")
        print("  3. All imports are correct")
        print("  4. ChromaDB dependencies are installed")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
