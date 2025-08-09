#!/usr/bin/env python3
"""
Simple test script for the Payment Gateway API
Run this after starting the server to test basic functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_signup():
    """Test user signup"""
    print("📝 Testing user signup...")
    signup_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json=signup_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ Signup successful!")
        print(f"User created: {response.json()}")
    else:
        print(f"❌ Signup failed: {response.text}")
    print()

def test_signin():
    """Test user signin"""
    print("🔑 Testing user signin...")
    signin_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/signin",
        json=signin_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Signin successful!")
        token_data = response.json()
        print(f"Token: {token_data['access_token'][:50]}...")
        return token_data['access_token']
    else:
        print(f"❌ Signin failed: {response.text}")
        return None

def test_profile(token):
    """Test protected profile endpoint"""
    print("👤 Testing profile endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/auth/profile",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Profile access successful!")
        print(f"User profile: {response.json()}")
    else:
        print(f"❌ Profile access failed: {response.text}")
    print()

def test_create_payment(token):
    """Test payment creation"""
    print("💳 Testing payment creation...")
    headers = {"Authorization": f"Bearer {token}"}
    payment_data = {
        "amount": 1000.00,
        "currency": "INR",
        "description": "Test payment"
    }
    
    response = requests.post(
        f"{BASE_URL}/payments/create-payment",
        json=payment_data,
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Payment creation successful!")
        payment_info = response.json()
        print(f"Payment ID: {payment_info.get('payment_id')}")
        print(f"Order ID: {payment_info.get('order_id')}")
        return payment_info
    else:
        print(f"❌ Payment creation failed: {response.text}")
        return None

def test_get_payments(token):
    """Test getting user payments"""
    print("📋 Testing get payments...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/payments/my-payments",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        payments = response.json()
        print(f"✅ Found {len(payments)} payments")
        for payment in payments:
            print(f"  - Payment ID: {payment['id']}, Status: {payment['status']}")
    else:
        print(f"❌ Get payments failed: {response.text}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting Payment Gateway API Tests")
    print("=" * 50)
    
    # Test health endpoint
    test_health()
    
    # Test authentication
    test_signup()
    token = test_signin()
    
    if token:
        # Test protected endpoints
        test_profile(token)
        test_create_payment(token)
        test_get_payments(token)
    
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main()
