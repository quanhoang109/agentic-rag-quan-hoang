"""
Lesson 2: Exercise - Understanding Embeddings
Complete the TODOs below to practice working with embeddings

Student Name: _______________
Date: _______________
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np
from typing import List

# Load environment variables
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    TODO: Implement this function to generate embeddings using OpenAI API

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
    pass


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    TODO: Implement cosine similarity calculation

    Formula: cos(θ) = (A · B) / (||A|| × ||B||)

    Steps:
    1. Convert vectors to numpy arrays
    2. Calculate dot product using np.dot()
    3. Calculate magnitudes using np.linalg.norm()
    4. Divide dot product by product of magnitudes

    Args:
        vec1: First embedding vector
        vec2: Second embedding vector

    Returns:
        Cosine similarity score between -1 and 1
    """
    # TODO: Implement this function
    pass


def normalize_embedding(embedding: List[float]) -> np.ndarray:
    """
    TODO: Implement vector normalization

    Steps:
    1. Convert embedding to numpy array
    2. Calculate the magnitude (L2 norm) using np.linalg.norm()
    3. Divide the vector by its magnitude

    Args:
        embedding: The embedding vector to normalize

    Returns:
        Normalized embedding as numpy array
    """
    # TODO: Implement this function
    pass


def exercise_1_generate_embeddings():
    """
    Exercise 1: Generate and inspect embeddings

    TODO:
    1. Generate embeddings for all three product descriptions
    2. Print the dimension of each embedding
    3. Print the first 5 values of the iPhone embedding
    """
    print("=" * 70)
    print("EXERCISE 1: Generate Embeddings")
    print("=" * 70)

    products = [
        "iPhone 15 Pro Max 256GB",
        "Samsung Galaxy S24 Ultra 512GB",
        "OPPO Find N3 5G"
    ]

    print("\nProducts:")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product}")

    # TODO: Generate embeddings for each product
    # embeddings = []
    # for product in products:
    #     embedding = get_embedding(product)
    #     embeddings.append(embedding)
    #     print(f"\nProduct: {product}")
    #     print(f"  Dimension: ???")

    print("\n⚠ TODO: Complete this exercise")


def exercise_2_calculate_similarity():
    """
    Exercise 2: Calculate similarity between products

    TODO:
    1. Generate embeddings for the query and all products
    2. Calculate cosine similarity between query and each product
    3. Print the results
    4. Which product is most similar to the query?
    """
    print("\n\n" + "=" * 70)
    print("EXERCISE 2: Calculate Similarity")
    print("=" * 70)

    query = "Tôi muốn mua điện thoại iPhone"
    products = [
        "iPhone 15 Pro Max 256GB - Titanium Blue",
        "Samsung Galaxy S24 Ultra 512GB",
        "MacBook Pro 14 inch M3"
    ]

    print(f"\nQuery: '{query}'")
    print("\nProducts:")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product}")

    # TODO: Generate query embedding
    # query_embedding = get_embedding(query)

    # TODO: For each product:
    #   1. Generate embedding
    #   2. Calculate cosine similarity with query
    #   3. Print the similarity score

    print("\n⚠ TODO: Complete this exercise")
    print("Expected: iPhone should have highest similarity")


def exercise_3_normalization():
    """
    Exercise 3: Understand normalization

    TODO:
    1. Generate an embedding for the text
    2. Calculate its magnitude before normalization
    3. Normalize the embedding
    4. Calculate magnitude after normalization (should be 1.0)
    5. Verify that normalized magnitude equals 1.0
    """
    print("\n\n" + "=" * 70)
    print("EXERCISE 3: Vector Normalization")
    print("=" * 70)

    text = "Samsung Galaxy S24 smartphone"
    print(f"\nText: '{text}'")

    # TODO: Generate embedding
    # embedding = get_embedding(text)

    # TODO: Calculate magnitude before normalization
    # magnitude_before = ???
    # print(f"Magnitude before normalization: {magnitude_before}")

    # TODO: Normalize the embedding
    # normalized = normalize_embedding(embedding)

    # TODO: Calculate magnitude after normalization
    # magnitude_after = ???
    # print(f"Magnitude after normalization: {magnitude_after}")

    # TODO: Verify it's close to 1.0
    # is_normalized = abs(magnitude_after - 1.0) < 0.0001
    # print(f"Is properly normalized: {is_normalized}")

    print("\n⚠ TODO: Complete this exercise")


def exercise_4_find_most_similar():
    """
    Exercise 4: Find the most similar product

    TODO:
    1. Generate embeddings for the query and all products
    2. Normalize all embeddings
    3. Calculate similarities
    4. Find and print the most similar product
    """
    print("\n\n" + "=" * 70)
    print("EXERCISE 4: Find Most Similar Product")
    print("=" * 70)

    query = "smartphone có camera tốt nhất"
    products = [
        "iPhone 15 Pro Max - Camera 48MP Pro",
        "Samsung Galaxy S24 Ultra - Camera 200MP",
        "OPPO Find X6 Pro - Camera Hasselblad",
        "Nokia 3210 4G - Camera 2MP",
        "MacBook Pro 14 inch"
    ]

    print(f"\nQuery: '{query}'")
    print("\nProducts:")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product}")

    # TODO: Implement similarity search
    # 1. Generate and normalize query embedding
    # 2. For each product:
    #    - Generate and normalize embedding
    #    - Calculate similarity
    #    - Store (product, similarity) pair
    # 3. Find the product with highest similarity
    # 4. Print results

    print("\n⚠ TODO: Complete this exercise")
    print("\nExpected output:")
    print("  Most similar product: [one of the camera phones]")
    print("  Similarity score: [between 0 and 1]")


def bonus_exercise_multilingual():
    """
    BONUS Exercise: Test multilingual similarity

    TODO:
    1. Generate embeddings for the same meaning in different languages
    2. Calculate similarity between them
    3. Compare with similarity to unrelated text
    """
    print("\n\n" + "=" * 70)
    print("BONUS EXERCISE: Multilingual Similarity")
    print("=" * 70)

    texts = {
        "vietnamese": "Tôi muốn mua điện thoại mới",
        "english": "I want to buy a new phone",
        "spanish": "Quiero comprar un teléfono nuevo",
        "unrelated": "The weather is nice today"
    }

    print("\nTexts:")
    for lang, text in texts.items():
        print(f"  {lang}: '{text}'")

    # TODO: Calculate similarities between:
    #   - Vietnamese and English
    #   - Vietnamese and Spanish
    #   - English and unrelated
    # Which pairs have highest similarity?

    print("\n⚠ TODO: Complete this bonus exercise")


def main():
    """
    Run all exercises.
    Uncomment exercises as you complete them.
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "LESSON 2: EXERCISES" + " " * 29 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\nComplete the TODO items in each exercise function.")
    print("Uncomment the function calls below as you complete them.\n")

    try:
        # Uncomment as you complete each exercise
        exercise_1_generate_embeddings()
        # exercise_2_calculate_similarity()
        # exercise_3_normalization()
        # exercise_4_find_most_similar()
        # bonus_exercise_multilingual()

        print("\n\n" + "=" * 70)
        print("Exercises completed! Run verify.py to check your solutions.")
        print("=" * 70)
        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. OPENAI_API_KEY is set in .env file")
        print("  2. You've implemented the required functions")
        print("  3. All imports are correct")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
