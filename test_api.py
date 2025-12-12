#!/usr/bin/env python3
"""
Simple API testing script for Wedding Company Management Service
Run this script to test basic functionality of the API endpoints.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"
test_org = {
    "organization_name": "TestWeddingCo",
    "email": "admin@testweddingco.com",
    "password": "testpassword123"
}

def test_create_organization():
    """Test organization creation"""
    print("🧪 Testing Organization Creation...")
    try:
        response = requests.post(f"{BASE_URL}/org/create", json=test_org)
        if response.status_code == 200:
            data = response.json()
            print("✅ Organization created successfully!")
            print(f"   Organization: {data['data']['organization_name']}")
            print(f"   Collection: {data['data']['collection_name']}")
            return True
        else:
            print(f"❌ Failed to create organization: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_organization():
    """Test organization retrieval"""
    print("\n🧪 Testing Organization Retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/org/get", params={"organization_name": test_org["organization_name"]})
        if response.status_code == 200:
            data = response.json()
            print("✅ Organization retrieved successfully!")
            print(f"   Organization: {data['data']['organization_name']}")
            return True
        else:
            print(f"❌ Failed to get organization: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_admin_login():
    """Test admin login"""
    print("\n🧪 Testing Admin Login...")
    try:
        login_data = {
            "email": test_org["email"],
            "password": test_org["password"]
        }
        response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"   Token: {data['access_token'][:50]}...")
            return data['access_token']
        else:
            print(f"❌ Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_wedding_operations(token):
    """Test wedding CRUD operations"""
    print("\n🧪 Testing Wedding Operations...")

    headers = {"Authorization": f"Bearer {token}"}

    # Create wedding
    wedding_data = {
        "bride_name": "Emma Watson",
        "groom_name": "Tom Hanks",
        "wedding_date": "2025-06-15",
        "venue": "Grand Plaza Hotel",
        "budget": 75000.00
    }

    try:
        response = requests.post(f"{BASE_URL}/weddings/", json=wedding_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            wedding_id = data['data']['id']
            print("✅ Wedding created successfully!")
            print(f"   Wedding ID: {wedding_id}")

            # Get wedding
            response = requests.get(f"{BASE_URL}/weddings/{wedding_id}", headers=headers)
            if response.status_code == 200:
                print("✅ Wedding retrieved successfully!")
            else:
                print(f"❌ Failed to get wedding: {response.text}")

            # List weddings
            response = requests.get(f"{BASE_URL}/weddings/", headers=headers)
            if response.status_code == 200:
                weddings = response.json()['data']
                print(f"✅ Weddings listed successfully! Count: {len(weddings)}")

            # Update wedding
            update_data = {"budget": 80000.00}
            response = requests.put(f"{BASE_URL}/weddings/{wedding_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                print("✅ Wedding updated successfully!")
            else:
                print(f"❌ Failed to update wedding: {response.text}")

            # Delete wedding
            response = requests.delete(f"{BASE_URL}/weddings/{wedding_id}", headers=headers)
            if response.status_code == 200:
                print("✅ Wedding deleted successfully!")
            else:
                print(f"❌ Failed to delete wedding: {response.text}")

            return True
        else:
            print(f"❌ Failed to create wedding: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    print("\n🧪 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def cleanup_organization(token):
    """Clean up test organization"""
    print("\n🧪 Cleaning up test organization...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{BASE_URL}/org/delete", params={"organization_name": test_org["organization_name"]}, headers=headers)
        if response.status_code == 200:
            print("✅ Test organization deleted successfully!")
            return True
        else:
            print(f"❌ Failed to delete organization: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Wedding Company API Tests")
    print("=" * 50)

    # Test health check
    if not test_health_check():
        print("\n❌ Health check failed. Is the server running?")
        sys.exit(1)

    # Test organization creation
    if not test_create_organization():
        print("\n❌ Organization creation failed. Stopping tests.")
        sys.exit(1)

    # Test organization retrieval
    if not test_get_organization():
        print("\n❌ Organization retrieval failed.")

    # Test admin login
    token = test_admin_login()
    if not token:
        print("\n❌ Admin login failed. Stopping tests.")
        sys.exit(1)

    # Test wedding operations
    if not test_wedding_operations(token):
        print("\n❌ Wedding operations failed.")

    # Clean up
    cleanup_organization(token)

    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n📖 API Documentation: http://localhost:8000/docs")
    print("📚 ReDoc Documentation: http://localhost:8000/redoc")

if __name__ == "__main__":
    main()