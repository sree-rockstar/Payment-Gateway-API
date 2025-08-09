#!/usr/bin/env python3
"""
Test script to verify Swagger UI authorization is working properly.
This script tests the authentication flow and protected endpoints.
"""

import requests
import json
import sys

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_signup():
    """Test user signup."""
    print("\n🔍 Testing user signup...")
    signup_data = {
        "email": "swagger_test@example.com",
        "password": "testpass123",
        "full_name": "Swagger Test User"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=signup_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print("✅ User signup successful")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("✅ User already exists (expected)")
            return True
        else:
            print(f"❌ Signup failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return False

def test_signin():
    """Test user signin and get token."""
    print("\n🔍 Testing user signin...")
    signin_data = {
        "email": "swagger_test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signin",
            json=signin_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print("✅ User signin successful")
                print(f"🔑 Token: {token[:50]}...")
                return token
            else:
                print("❌ No token in response")
                return None
        else:
            print(f"❌ Signin failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Signin error: {e}")
        return None

def test_protected_endpoint(token):
    """Test protected endpoint with Bearer token."""
    print("\n🔍 Testing protected endpoint with Bearer token...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Protected endpoint working with Bearer token")
            print(f"👤 User: {data.get('email')} - {data.get('full_name')}")
            return True
        else:
            print(f"❌ Protected endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False

def test_swagger_ui_info():
    """Provide information about Swagger UI testing."""
    print("\n" + "="*60)
    print("🎯 SWAGGER UI TESTING INSTRUCTIONS")
    print("="*60)
    print("1. Open Swagger UI: http://localhost:8000/docs")
    print("2. Click the 'Authorize' button (🔒) at the top right")
    print("3. In the 'Value' field, enter: Bearer YOUR_TOKEN")
    print("4. Replace YOUR_TOKEN with the token from the test above")
    print("5. Click 'Authorize' then 'Close'")
    print("6. Try the GET /auth/profile endpoint")
    print("7. Check the browser's Network tab to verify Authorization header")
    print("\n🔧 Troubleshooting:")
    print("- Make sure to include 'Bearer ' before your token")
    print("- Clear browser cache if Swagger seems stuck")
    print("- Check browser console for any JavaScript errors")
    print("- Verify the token is not expired")
    print("="*60)

def main():
    """Main test function."""
    print("🚀 Testing Payment Gateway API Authentication")
    print("="*50)
    
    # Test health
    if not test_health():
        print("❌ Health check failed. Is the API running?")
        sys.exit(1)
    
    # Test signup
    if not test_signup():
        print("❌ Signup test failed")
        sys.exit(1)
    
    # Test signin and get token
    token = test_signin()
    if not token:
        print("❌ Signin test failed")
        sys.exit(1)
    
    # Test protected endpoint
    if not test_protected_endpoint(token):
        print("❌ Protected endpoint test failed")
        sys.exit(1)
    
    # Provide Swagger UI instructions
    test_swagger_ui_info()
    
    print("\n✅ All tests passed! Swagger UI should now work properly.")
    print(f"🔑 Use this token in Swagger UI: {token}")

if __name__ == "__main__":
    main()
