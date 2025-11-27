"""
Automated verification for Lesson 3 exercises.
Run: python solution/verify.py
"""

import chromadb
import sys
import os
import shutil

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
        print(f"   - Returns list of {len(embedding)} floats")
        print(f"   - Sample values: {embedding[:3]}")
        return True

    except AssertionError as e:
        print(f"❌ FAIL: {e}")
        return False
    except Exception as e:
        print(f"❌ FAIL: Unexpected error - {e}")
        return False


def test_chromadb_setup():
    """Test 2: Verify ChromaDB client and collection setup."""
    print("\n" + "=" * 70)
    print("TEST 2: ChromaDB Setup and Insertion")
    print("=" * 70)

    try:
        # Clean up any existing db for testing
        if os.path.exists("db"):
            shutil.rmtree("db")
            print("   Cleaned up previous database")

        # Run exercise 1
        print("\n   Running exercise_1_insert_documents()...")
        exercise_1_insert_documents()

        # Verify collection exists
        client = chromadb.PersistentClient(path="db")
        collection = client.get_collection(name="products")

        # Verify document count
        count = collection.count()
        assert count == 3, f"Should have 3 documents, got {count}"

        # Verify metadata structure
        result = collection.get(ids=["1"])
        metadata = result['metadatas'][0]

        assert 'name' in metadata, "Metadata should have 'name' field"
        assert 'price' in metadata, "Metadata should have 'price' field"
        assert 'category' in metadata, "Metadata should have 'category' field"

        print("\n✅ PASS: ChromaDB setup and insertion works")
        print(f"   - Collection created: '{collection.name}'")
        print(f"   - Documents inserted: {count}")
        print(f"   - Metadata structure: {list(metadata.keys())}")
        return True

    except AssertionError as e:
        print(f"\n❌ FAIL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ FAIL: Unexpected error - {e}")
        print("   Make sure exercise_1_insert_documents() is properly implemented")
        return False


def test_vector_search():
    """Test 3: Verify vector search works."""
    print("\n" + "=" * 70)
    print("TEST 3: Vector Search")
    print("=" * 70)

    try:
        # Verify collection has data from test 2
        client = chromadb.PersistentClient(path="db")
        collection = client.get_collection(name="products")

        assert collection.count() > 0, "Collection should have documents from previous test"

        # Test basic query
        query_embedding = get_embedding("smartphone")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )

        # Verify results structure
        assert 'metadatas' in results, "Results should have 'metadatas'"
        assert 'distances' in results, "Results should have 'distances'"
        assert len(results['metadatas'][0]) > 0, "Should return at least one result"

        # Verify distances are reasonable
        for distance in results['distances'][0]:
            assert 0 <= distance <= 2, f"Cosine distance should be 0-2, got {distance}"

        print("\n✅ PASS: Vector search works")
        print(f"   - Results returned: {len(results['metadatas'][0])}")
        print(f"   - Distance range: {min(results['distances'][0]):.4f} - {max(results['distances'][0]):.4f}")

        print("\n   Running exercise_2_vector_search()...")
        exercise_2_vector_search()

        return True

    except AssertionError as e:
        print(f"\n❌ FAIL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ FAIL: Unexpected error - {e}")
        print("   Make sure exercise_2_vector_search() is properly implemented")
        return False


def test_update_delete():
    """Test 4: Verify update and delete operations."""
    print("\n" + "=" * 70)
    print("TEST 4: Update and Delete Operations")
    print("=" * 70)

    try:
        client = chromadb.PersistentClient(path="db")
        collection = client.get_collection(name="products")

        initial_count = collection.count()
        print(f"\n   Initial document count: {initial_count}")

        # Test update
        print("\n   Running exercise_3_update_documents()...")
        exercise_3_update_documents()

        # Verify update
        result = collection.get(ids=["1"])
        updated_metadata = result['metadatas'][0]

        assert updated_metadata['price'] == "28990000", \
            f"Price should be updated to '28990000', got '{updated_metadata['price']}'"

        print(f"   ✓ Update verified: price changed to {updated_metadata['price']}")

        # Test delete
        print("\n   Running exercise_4_delete_documents()...")
        exercise_4_delete_documents()

        # Verify deletion
        final_count = collection.count()

        assert final_count == initial_count - 1, \
            f"Should have {initial_count - 1} documents after deletion, got {final_count}"

        print(f"   ✓ Delete verified: count {initial_count} → {final_count}")

        print("\n✅ PASS: Update and delete work correctly")
        print(f"   - Update: Metadata changed successfully")
        print(f"   - Delete: Document removed successfully")
        return True

    except AssertionError as e:
        print(f"\n❌ FAIL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ FAIL: Unexpected error - {e}")
        print("   Make sure exercise_3 and exercise_4 are properly implemented")
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
        print("\nYou have successfully:")
        print("  ✓ Implemented get_embedding() function")
        print("  ✓ Set up ChromaDB with persistent storage")
        print("  ✓ Inserted documents with embeddings and metadata")
        print("  ✓ Performed vector similarity searches")
        print("  ✓ Updated and deleted documents")
        print("\nYou're ready for Lesson 4: Building Basic RAG Pipeline!")
    else:
        failed = total - passed
        print(f"\n⚠ {failed} test(s) failed. Keep working on the exercises!")
        print("\nTips:")
        print("  - Review the error messages above")
        print("  - Check instructions.md for implementation details")
        print("  - Compare with solution/chromadb_complete.py")
        print("  - Make sure all TODOs are completed")

    print("\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    exit(main())
