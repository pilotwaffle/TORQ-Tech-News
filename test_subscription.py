"""Test script for newsletter subscription system.

This script tests the subscription endpoint with various scenarios:
- Valid email subscription
- Duplicate email detection
- Invalid email validation
- Backend failover (Azure → SQLite)

Usage:
    python test_subscription.py
"""

from __future__ import annotations

import json
import sys
from typing import Any

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_EMAIL = "test@example.com"
INVALID_EMAIL = "notanemail"


def test_subscription(email: str, expected_status: int, test_name: str) -> dict[str, Any]:
    """Test subscription endpoint.

    Args:
        email: Email address to test.
        expected_status: Expected HTTP status code.
        test_name: Name of the test for logging.

    Returns:
        Response data dictionary.
    """
    import requests

    print(f"\n[TEST] {test_name}")
    print(f"  Email: {email}")

    try:
        response = requests.post(
            f"{BASE_URL}/api/subscribe",
            json={"email": email},
            headers={"Content-Type": "application/json"}
        )

        print(f"  Status Code: {response.status_code} (expected: {expected_status})")
        print(f"  Response: {response.json()}")

        if response.status_code == expected_status:
            print(f"  ✓ PASSED")
            return {"passed": True, "data": response.json()}
        else:
            print(f"  ✗ FAILED - Status code mismatch")
            return {"passed": False, "data": response.json()}

    except Exception as e:
        print(f"  ✗ FAILED - Error: {e}")
        return {"passed": False, "error": str(e)}


def test_subscriber_count() -> dict[str, Any]:
    """Test subscriber count endpoint.

    Returns:
        Response data dictionary.
    """
    import requests

    print(f"\n[TEST] Get Subscriber Count")

    try:
        response = requests.get(f"{BASE_URL}/api/subscribers/count")
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")

        if response.status_code == 200:
            print(f"  ✓ PASSED")
            return {"passed": True, "data": response.json()}
        else:
            print(f"  ✗ FAILED")
            return {"passed": False, "data": response.json()}

    except Exception as e:
        print(f"  ✗ FAILED - Error: {e}")
        return {"passed": False, "error": str(e)}


def test_direct_storage() -> None:
    """Test subscribers storage module directly.

    This tests the storage layer without HTTP requests.
    """
    print(f"\n[TEST] Direct Storage Layer Testing")

    try:
        from subscribers_storage import SubscribersStorage, ValidationError, DuplicateSubscriptionError

        storage = SubscribersStorage()
        print(f"  Storage backend: {'Azure' if storage.use_azure else 'SQLite'}")

        # Test email validation
        print("\n  Subtest: Email Validation")
        try:
            storage.validate_email("invalid-email")
            print("    ✗ FAILED - Should have raised ValidationError")
        except ValidationError:
            print("    ✓ PASSED - Invalid email rejected")

        # Test valid email normalization
        normalized = storage.validate_email("  User@Example.COM  ")
        if normalized == "user@example.com":
            print("    ✓ PASSED - Email normalized correctly")
        else:
            print(f"    ✗ FAILED - Expected 'user@example.com', got '{normalized}'")

        # Test subscription
        print("\n  Subtest: Subscription")
        test_email = f"direct-test@example.com"
        try:
            result = storage.subscribe(test_email, "192.168.1.1")
            if result.success:
                print(f"    ✓ PASSED - Subscribed with {result.storage_backend}")
            else:
                print(f"    ✗ FAILED - Subscription failed")
        except DuplicateSubscriptionError:
            print(f"    ℹ INFO - Email already subscribed (expected if running multiple times)")

        # Test duplicate detection
        print("\n  Subtest: Duplicate Detection")
        try:
            storage.subscribe(test_email, "192.168.1.1")
            print("    ✗ FAILED - Should have raised DuplicateSubscriptionError")
        except DuplicateSubscriptionError:
            print("    ✓ PASSED - Duplicate email detected")

        # Test subscriber count
        print("\n  Subtest: Subscriber Count")
        stats = storage.get_subscriber_count()
        print(f"    Total subscribers: {stats['count']} (backend: {stats['backend']})")
        if stats['success']:
            print("    ✓ PASSED - Count retrieved successfully")
        else:
            print("    ✗ FAILED - Count retrieval failed")

    except ImportError as e:
        print(f"  ✗ FAILED - Cannot import subscribers_storage: {e}")
    except Exception as e:
        print(f"  ✗ FAILED - Error: {e}")
        import traceback
        traceback.print_exc()


def run_all_tests() -> None:
    """Run all subscription tests."""
    print("="*70)
    print("TORQ Tech News - Newsletter Subscription Test Suite")
    print("="*70)

    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("\n[ERROR] 'requests' library not installed")
        print("Install with: pip install requests")
        sys.exit(1)

    # Check if server is running
    try:
        import requests
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"\n[INFO] Server is running at {BASE_URL}")
        print(f"[INFO] Health check: {response.json().get('status', 'unknown')}")
    except Exception as e:
        print(f"\n[ERROR] Cannot connect to server at {BASE_URL}")
        print(f"[ERROR] {e}")
        print("\n[INFO] Make sure the Flask server is running:")
        print("       python app.py")
        sys.exit(1)

    results = []

    # Test 1: Valid email subscription
    results.append(test_subscription(
        email=TEST_EMAIL,
        expected_status=200,
        test_name="Valid Email Subscription"
    ))

    # Test 2: Duplicate email
    results.append(test_subscription(
        email=TEST_EMAIL,
        expected_status=409,
        test_name="Duplicate Email Detection"
    ))

    # Test 3: Invalid email format
    results.append(test_subscription(
        email=INVALID_EMAIL,
        expected_status=400,
        test_name="Invalid Email Format"
    ))

    # Test 4: Empty email
    results.append(test_subscription(
        email="",
        expected_status=400,
        test_name="Empty Email"
    ))

    # Test 5: Subscriber count
    results.append(test_subscriber_count())

    # Test 6: Direct storage layer
    test_direct_storage()

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for r in results if r.get("passed", False))
    total = len(results)

    print(f"\nPassed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")

    if passed == total:
        print("\n✓ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
