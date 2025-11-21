"""
Lesson 2: Verification Script
Checks if student's exercise implementation is correct
"""

import sys
import os
from typing import List
import numpy as np

# Add exercises directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exercises'))

try:
    from my_embeddings import (
        get_embedding,
        cosine_similarity,
        normalize_embedding
    )
except ImportError as e:
    print(f"❌ Error importing functions: {e}")
    print("\nMake sure you've implemented all functions in exercises/my_embeddings.py")
    sys.exit(1)


def check_get_embedding():
    """Verify get_embedding function works correctly"""
    print("\n" + "=" * 70)
    print("TEST 1: get_embedding() function")
    print("=" * 70)

    try:
        text = "test embedding"
        result = get_embedding(text)

        # Check if result is a list
        if not isinstance(result, list):
            print(f"❌ FAIL: Expected list, got {type(result)}")
            return False

        # Check dimension (should be 1536 for text-embedding-3-small)
        if len(result) != 1536:
            print(f"❌ FAIL: Expected 1536 dimensions, got {len(result)}")
            return False

        # Check if values are floats
        if not all(isinstance(x, float) for x in result[:10]):
            print(f"❌ FAIL: Expected floats in embedding vector")
            return False

        print(f"✓ Returns correct type: list")
        print(f"✓ Correct dimensions: {len(result)}")
        print(f"✓ Contains float values")
        print(f"✓ Sample values: {result[:3]}")
        print("\n✅ PASS: get_embedding() works correctly")
        return True

    except NotImplementedError:
        print("❌ FAIL: Function not implemented (still has 'pass')")
        return False
    except Exception as e:
        print(f"❌ FAIL: Error - {e}")
        return False


def check_cosine_similarity():
    """Verify cosine_similarity function works correctly"""
    print("\n" + "=" * 70)
    print("TEST 2: cosine_similarity() function")
    print("=" * 70)

    try:
        # Test with known vectors
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        vec3 = [0.0, 1.0, 0.0]

        # Identical vectors should have similarity = 1.0
        sim_identical = cosine_similarity(vec1, vec2)
        if not (0.99 < sim_identical < 1.01):
            print(f"❌ FAIL: Identical vectors should have similarity ≈ 1.0, got {sim_identical}")
            return False

        # Orthogonal vectors should have similarity = 0.0
        sim_orthogonal = cosine_similarity(vec1, vec3)
        if not (-0.01 < sim_orthogonal < 0.01):
            print(f"❌ FAIL: Orthogonal vectors should have similarity ≈ 0.0, got {sim_orthogonal}")
            return False

        # Test with real embeddings
        emb1 = get_embedding("iPhone 15 Pro")
        emb2 = get_embedding("iPhone 15 Pro Max")
        emb3 = get_embedding("laptop computer")

        sim_similar = cosine_similarity(emb1, emb2)
        sim_different = cosine_similarity(emb1, emb3)

        if not (-1.0 <= sim_similar <= 1.0):
            print(f"❌ FAIL: Similarity should be between -1 and 1, got {sim_similar}")
            return False

        if sim_similar <= sim_different:
            print(f"❌ FAIL: Similar items should have higher similarity")
            print(f"  iPhone vs iPhone: {sim_similar}")
            print(f"  iPhone vs Laptop: {sim_different}")
            return False

        print(f"✓ Identical vectors: {sim_identical:.4f} ≈ 1.0")
        print(f"✓ Orthogonal vectors: {sim_orthogonal:.4f} ≈ 0.0")
        print(f"✓ Similar items: {sim_similar:.4f}")
        print(f"✓ Different items: {sim_different:.4f}")
        print(f"✓ Correctly ranks similar > different")
        print("\n✅ PASS: cosine_similarity() works correctly")
        return True

    except NotImplementedError:
        print("❌ FAIL: Function not implemented (still has 'pass')")
        return False
    except Exception as e:
        print(f"❌ FAIL: Error - {e}")
        return False


def check_normalize_embedding():
    """Verify normalize_embedding function works correctly"""
    print("\n" + "=" * 70)
    print("TEST 3: normalize_embedding() function")
    print("=" * 70)

    try:
        # Test with simple vector
        vec = [3.0, 4.0]
        normalized = normalize_embedding(vec)

        # Check if it's a numpy array
        if not isinstance(normalized, np.ndarray):
            print(f"❌ FAIL: Expected numpy array, got {type(normalized)}")
            return False

        # Check magnitude is 1.0
        magnitude = np.linalg.norm(normalized)
        if not (0.99 < magnitude < 1.01):
            print(f"❌ FAIL: Normalized vector should have magnitude ≈ 1.0, got {magnitude}")
            return False

        # Test with real embedding
        embedding = get_embedding("test text")
        original_magnitude = np.linalg.norm(embedding)
        normalized = normalize_embedding(embedding)
        normalized_magnitude = np.linalg.norm(normalized)

        if not (0.99 < normalized_magnitude < 1.01):
            print(f"❌ FAIL: Real embedding normalization failed")
            print(f"  Original magnitude: {original_magnitude}")
            print(f"  Normalized magnitude: {normalized_magnitude}")
            return False

        print(f"✓ Returns numpy array")
        print(f"✓ Simple vector [3, 4] normalized correctly")
        print(f"✓ Original embedding magnitude: {original_magnitude:.6f}")
        print(f"✓ Normalized magnitude: {normalized_magnitude:.6f} ≈ 1.0")
        print("\n✅ PASS: normalize_embedding() works correctly")
        return True

    except NotImplementedError:
        print("❌ FAIL: Function not implemented (still has 'pass')")
        return False
    except Exception as e:
        print(f"❌ FAIL: Error - {e}")
        return False


def check_exercise_completion():
    """Check if student completed the exercises"""
    print("\n" + "=" * 70)
    print("TEST 4: Exercise Completion Check")
    print("=" * 70)

    try:
        # Read the exercise file
        exercise_path = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'my_embeddings.py')
        with open(exercise_path, 'r') as f:
            content = f.read()

        # Count remaining TODOs
        todo_count = content.count('# TODO:') + content.count('⚠ TODO:')
        pass_count = content.count('    pass')

        print(f"\nExercise file analysis:")
        print(f"  Remaining TODO comments: {todo_count}")
        print(f"  Remaining 'pass' statements: {pass_count}")

        if pass_count > 4:  # Main functions should not have pass
            print(f"\n⚠ WARNING: Still have {pass_count} 'pass' statements")
            print(f"  Make sure to implement all exercise functions")
            return False

        if todo_count > 20:
            print(f"\n⚠ WARNING: Still have {todo_count} TODO comments")
            print(f"  Try to complete more exercises")
            return False

        print(f"\n✅ PASS: Good progress on exercises!")
        return True

    except Exception as e:
        print(f"⚠ Could not analyze exercise file: {e}")
        return True  # Don't fail the test for this


def main():
    """Run all verification tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 18 + "LESSON 2: VERIFICATION" + " " * 27 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\nChecking your exercise solutions...")

    results = []

    # Run all tests
    results.append(("get_embedding", check_get_embedding()))
    results.append(("cosine_similarity", check_cosine_similarity()))
    results.append(("normalize_embedding", check_normalize_embedding()))
    results.append(("exercises", check_exercise_completion()))

    # Summary
    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\nScore: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 Congratulations! All tests passed!")
        print("\nYou've successfully completed Lesson 2: Understanding Embeddings")
        print("\nKey achievements:")
        print("  ✓ Can generate embeddings using OpenAI API")
        print("  ✓ Can calculate semantic similarity")
        print("  ✓ Understand vector normalization")
        print("\nNext: Lesson 3 - Vector Databases (ChromaDB)")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Keep working on the exercises!")
        print("\nTips:")
        print("  1. Review the error messages above")
        print("  2. Check the solution code in solution/embeddings_demo.py")
        print("  3. Make sure all functions are implemented (no 'pass' statements)")
        print("  4. Test your functions individually before running verify.py")
        return 1


if __name__ == "__main__":
    exit(main())
