#!/usr/bin/env python3
"""
Razorpay Integration Test Script
Tests the payment gateway with Razorpay test credentials
"""

import requests
import json
import time
import os
from typing import Optional

BASE_URL = "http://localhost:8000"

# Test user credentials
TEST_USER = {
    "email": "razorpay_test@example.com",
    "full_name": "Razorpay Test User",
    "password": "testpassword123"
}

def print_separator(title: str):
    """Print a formatted separator"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_health():
    """Test API health"""
    print_separator("Testing API Health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"✅ Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def create_test_user():
    """Create a test user for payment testing"""
    print_separator("Creating Test User")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=TEST_USER,
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Test user created successfully")
            user_data = response.json()
            print(f"User ID: {user_data['id']}")
            print(f"Email: {user_data['email']}")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("ℹ️ Test user already exists")
            return True
        else:
            print(f"❌ User creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ User creation error: {e}")
        return False

def authenticate_user() -> Optional[str]:
    """Authenticate user and get JWT token"""
    print_separator("Authenticating User")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signin",
            json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            },
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            print("✅ Authentication successful")
            print(f"Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_create_payment(token: str):
    """Test payment creation with Razorpay"""
    print_separator("Testing Payment Creation")
    
    payment_data = {
        "amount": 1000.00,  # ₹1000
        "currency": "INR",
        "description": "Test payment via Razorpay"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(
            f"{BASE_URL}/payments/create-payment",
            json=payment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payment_info = response.json()
            print("✅ Payment creation successful!")
            print(f"Payment ID: {payment_info.get('payment_id')}")
            print(f"Order ID: {payment_info.get('order_id')}")
            print(f"Amount: ₹{payment_info.get('amount')}")
            print(f"Currency: {payment_info.get('currency')}")
            print(f"Razorpay Order ID: {payment_info.get('razorpay_order_id')}")
            
            # Store order ID for verification test
            return payment_info.get('order_id')
        else:
            print(f"❌ Payment creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Payment creation error: {e}")
        return None

def test_get_payments(token: str):
    """Test getting user payments"""
    print_separator("Testing Get Payments")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/payments/my-payments",
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            payments = response.json()
            print(f"✅ Found {len(payments)} payments")
            
            for i, payment in enumerate(payments, 1):
                print(f"\nPayment {i}:")
                print(f"  ID: {payment['id']}")
                print(f"  Order ID: {payment['order_id']}")
                print(f"  Amount: ₹{payment['amount']}")
                print(f"  Status: {payment['status']}")
                print(f"  Created: {payment['created_at']}")
        else:
            print(f"❌ Get payments failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Get payments error: {e}")

def test_profile(token: str):
    """Test protected profile endpoint"""
    print_separator("Testing Profile Access")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/profile",
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            profile = response.json()
            print("✅ Profile access successful!")
            print(f"User: {profile['full_name']}")
            print(f"Email: {profile['email']}")
        else:
            print(f"❌ Profile access failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Profile access error: {e}")

def test_razorpay_direct():
    """Test direct Razorpay API connection"""
    print_separator("Testing Direct Razorpay Connection")
    
    # This would require the actual Razorpay secret key
    # For now, we'll just test our API integration
    print("ℹ️ Direct Razorpay API testing requires the secret key")
    print("Testing through our API endpoints instead...")

def print_razorpay_info():
    """Print Razorpay integration information"""
    print_separator("Razorpay Integration Info")
    print("🔑 Test API Key: rzp_test_EnZ3V3m6bWKwsb")
    print("📚 Documentation: https://razorpay.com/docs/api/understand/")
    print("🧪 Test Mode: Enabled")
    print("\n💡 Test Card Details (for frontend testing):")
    print("  Card Number: 4111 1111 1111 1111")
    print("  Expiry: Any future date")
    print("  CVV: Any 3 digits")
    print("  Name: Any name")

def main():
    """Run comprehensive Razorpay integration tests"""
    print("🚀 Razorpay Payment Gateway Integration Test")
    print("=" * 60)
    
    # Check if server is running
    if not test_health():
        print("❌ Server is not running. Please start the server first:")
        print("   python run.py")
        return
    
    # Print Razorpay info
    print_razorpay_info()
    
    # Create test user
    if not create_test_user():
        print("❌ Failed to create test user")
        return
    
    # Authenticate user
    token = authenticate_user()
    if not token:
        print("❌ Failed to authenticate user")
        return
    
    # Test profile access
    test_profile(token)
    
    # Test payment creation
    order_id = test_create_payment(token)
    
    # Test get payments
    test_get_payments(token)
    
    # Test direct Razorpay connection
    test_razorpay_direct()
    
    print_separator("Test Summary")
    print("✅ All tests completed!")
    print("\n📋 Next Steps:")
    print("1. Set up your Razorpay secret key in .env file")
    print("2. Test payment verification with actual payment data")
    print("3. Integrate with frontend for complete payment flow")
    print("4. Check Razorpay dashboard for test transactions")

if __name__ == "__main__":
    main()
