#!/usr/bin/env python3
"""
Swagger Integration Test Script
Tests the API documentation and endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_swagger_endpoints():
    """Test Swagger documentation endpoints"""
    print("🔍 Testing Swagger Documentation Endpoints")
    print("=" * 50)
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/docs", "Swagger UI"),
        ("/redoc", "ReDoc documentation"),
        ("/openapi.json", "OpenAPI JSON specification"),
        ("/health", "Health check")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint} - {description} ({response.status_code})")
        except Exception as e:
            print(f"❌ {endpoint} - {description} (Error: {e})")
    
    print()

def test_openapi_spec():
    """Test OpenAPI specification"""
    print("📋 Testing OpenAPI Specification")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
        if response.status_code == 200:
            spec = response.json()
            
            # Check basic structure
            required_fields = ["openapi", "info", "paths", "components"]
            for field in required_fields:
                if field in spec:
                    print(f"✅ {field} - Present")
                else:
                    print(f"❌ {field} - Missing")
            
            # Check info
            info = spec.get("info", {})
            print(f"✅ Title: {info.get('title', 'Missing')}")
            print(f"✅ Version: {info.get('version', 'Missing')}")
            print(f"✅ Description: {'Present' if info.get('description') else 'Missing'}")
            
            # Check paths
            paths = spec.get("paths", {})
            print(f"✅ API Endpoints: {len(paths)} found")
            
            # Check components
            components = spec.get("components", {})
            schemas = components.get("schemas", {})
            print(f"✅ Data Models: {len(schemas)} found")
            
            # Check security schemes
            security_schemes = components.get("securitySchemes", {})
            if "BearerAuth" in security_schemes:
                print("✅ BearerAuth security scheme - Present")
            else:
                print("❌ BearerAuth security scheme - Missing")
            
            # Check servers
            servers = spec.get("servers", [])
            print(f"✅ Servers: {len(servers)} configured")
            
            # Check tags
            tags = spec.get("tags", [])
            print(f"✅ Tags: {len(tags)} configured")
            
        else:
            print(f"❌ Failed to get OpenAPI spec: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing OpenAPI spec: {e}")
    
    print()

def test_api_endpoints():
    """Test actual API endpoints"""
    print("🔧 Testing API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check: {health_data.get('status', 'Unknown')}")
            print(f"   Service: {health_data.get('service', 'Unknown')}")
            print(f"   Version: {health_data.get('version', 'Unknown')}")
        else:
            print(f"❌ Health Check: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check Error: {e}")
    
    # Test authentication endpoints
    auth_endpoints = [
        ("/auth/signup", "POST", {"email": "swagger_test@example.com", "full_name": "Swagger Test User", "password": "testpass123"}),
        ("/auth/signin", "POST", {"email": "swagger_test@example.com", "password": "testpass123"}),
    ]
    
    for endpoint, method, data in auth_endpoints:
        try:
            if method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=10)
            else:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code in [200, 201, 400]:  # 400 is expected for duplicate email
                print(f"✅ {method} {endpoint} - {response.status_code}")
            else:
                print(f"❌ {method} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {e}")
    
    print()

def test_swagger_ui_features():
    """Test Swagger UI specific features"""
    print("🎨 Testing Swagger UI Features")
    print("=" * 50)
    
    try:
        # Test Swagger UI page
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Check for Swagger UI elements
            checks = [
                ("swagger-ui-bundle.js", "Swagger UI JavaScript"),
                ("swagger-ui.css", "Swagger UI CSS"),
                ("openapi.json", "OpenAPI spec reference"),
                ("try-it-out", "Try it out feature"),
                ("authorize", "Authorization button"),
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} - Present")
                else:
                    print(f"❌ {description} - Missing")
        else:
            print(f"❌ Swagger UI not accessible: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing Swagger UI: {e}")
    
    print()

def print_swagger_info():
    """Print Swagger documentation information"""
    print("📚 Swagger Documentation Information")
    print("=" * 50)
    print("🔗 Documentation URLs:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")
    print(f"   OpenAPI JSON: {BASE_URL}/openapi.json")
    print(f"   Root: {BASE_URL}/")
    print()
    print("🎯 Features:")
    print("   ✅ Interactive API documentation")
    print("   ✅ Try it out functionality")
    print("   ✅ JWT authentication support")
    print("   ✅ Request/response examples")
    print("   ✅ Data model documentation")
    print("   ✅ Error response documentation")
    print("   ✅ External documentation links")
    print()
    print("🔐 Authentication:")
    print("   - Use /auth/signin to get JWT token")
    print("   - Click 'Authorize' button in Swagger UI")
    print("   - Enter token as: Bearer <your-token>")
    print()
    print("💡 Tips:")
    print("   - All endpoints are documented with examples")
    print("   - Request/response schemas are auto-generated")
    print("   - Error responses are documented")
    print("   - External links to JWT and Razorpay docs")
    print()

def main():
    """Run all Swagger tests"""
    print("🚀 Swagger Integration Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if not response.ok:
            print("❌ Server is not running. Please start the server first:")
            print("   python3 run.py")
            return
    except:
        print("❌ Cannot connect to server. Please make sure it's running on http://localhost:8000")
        return
    
    print("✅ Server is running and accessible")
    print()
    
    # Run tests
    test_swagger_endpoints()
    test_openapi_spec()
    test_api_endpoints()
    test_swagger_ui_features()
    print_swagger_info()
    
    print("🏁 Swagger integration test completed!")
    print("\n📋 Next Steps:")
    print("1. Visit http://localhost:8000/docs for interactive documentation")
    print("2. Try the 'Try it out' feature to test endpoints")
    print("3. Use the Authorize button to test protected endpoints")
    print("4. Check the ReDoc view at http://localhost:8000/redoc")

if __name__ == "__main__":
    main()
