# 🔗 Razorpay Integration Guide

This document provides comprehensive information about the Razorpay integration in the Payment Gateway API.

## 📋 Overview

The Payment Gateway API is now fully integrated with **Razorpay** using the provided test API key:
- **Test API Key**: `rzp_test_EnZ3V3m6bWKwsb`
- **Mode**: Test/Sandbox
- **Documentation**: [Razorpay API Docs](https://razorpay.com/docs/api/understand/)

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your Razorpay credentials
RAZORPAY_KEY_ID=rzp_test_EnZ3V3m6bWKwsb
RAZORPAY_KEY_SECRET=your_razorpay_test_secret_key
```

### 2. Start the Application

```bash
# Start MongoDB
mongod

# Start the API server
python3 run.py
```

### 3. Test the Integration

```bash
# Run comprehensive Razorpay tests
python3 test_razorpay.py

# Or use the frontend test page
open test_frontend.html
```

## 🔧 API Endpoints

### Payment Creation
```http
POST /payments/create-payment
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "amount": 1000.00,
  "currency": "INR",
  "description": "Test payment"
}
```

**Response:**
```json
{
  "payment_id": "mongodb_id",
  "order_id": "order_xxx",
  "amount": 1000.00,
  "currency": "INR",
  "razorpay_order_id": "order_xxx"
}
```

### Payment Verification
```http
POST /payments/verify-payment
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "razorpay_payment_id": "pay_xxx",
  "razorpay_order_id": "order_xxx",
  "razorpay_signature": "signature_xxx"
}
```

## 💳 Test Card Details

For testing payments in the frontend:

| Field | Value |
|-------|-------|
| **Card Number** | `4111 1111 1111 1111` |
| **Expiry** | Any future date |
| **CVV** | Any 3 digits |
| **Name** | Any name |

## 🧪 Testing Methods

### 1. Automated Test Script
```bash
python3 test_razorpay.py
```

This script will:
- ✅ Test API health
- ✅ Create test user
- ✅ Authenticate and get JWT token
- ✅ Create payment with Razorpay
- ✅ Test payment verification
- ✅ Check payment records

### 2. Frontend Test Page
Open `test_frontend.html` in your browser for a complete UI testing experience.

### 3. Manual API Testing
Use tools like Postman or curl:

```bash
# Create payment
curl -X POST "http://localhost:8000/payments/create-payment" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":1000,"currency":"INR","description":"Test"}'
```

## 🔐 Authentication Flow

1. **Sign Up**: Create user account
2. **Sign In**: Get JWT token
3. **Use Token**: Include in Authorization header for protected endpoints

```bash
# Sign up
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"password123"}'

# Sign in
curl -X POST "http://localhost:8000/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 📊 Database Schema

### Payments Collection
```json
{
  "_id": "ObjectId",
  "order_id": "order_xxx",
  "amount": 1000.00,
  "currency": "INR",
  "status": "pending|completed|failed",
  "user_id": "user_object_id",
  "description": "Payment description",
  "razorpay_payment_id": "pay_xxx",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 🔄 Payment Flow

1. **Create Payment Order**
   - User requests payment creation
   - API creates Razorpay order
   - Returns order details to frontend

2. **Process Payment**
   - Frontend opens Razorpay checkout
   - User completes payment
   - Razorpay returns payment details

3. **Verify Payment**
   - Frontend sends payment verification
   - API verifies signature with Razorpay
   - Updates payment status in database

## 🛡️ Security Features

- **JWT Authentication**: All payment endpoints are protected
- **Signature Verification**: Razorpay signatures are verified
- **Password Hashing**: bcrypt for secure password storage
- **Input Validation**: Pydantic models for data validation

## 📈 Monitoring & Debugging

### Check Payment Status
```bash
# Get user payments
curl -X GET "http://localhost:8000/payments/my-payments" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## 🚨 Common Issues

### 1. Razorpay Connection Error
**Error**: `Failed to create payment order`
**Solution**: Check your Razorpay credentials in `.env` file

### 2. Authentication Error
**Error**: `Could not validate credentials`
**Solution**: Make sure you're including the JWT token in Authorization header

### 3. Payment Verification Failed
**Error**: `Invalid payment signature`
**Solution**: Ensure you're using the correct payment data from Razorpay

## 🔗 Useful Links

- [Razorpay API Documentation](https://razorpay.com/docs/api/understand/)
- [Razorpay Dashboard](https://dashboard.razorpay.com)
- [Test Mode vs Live Mode](https://razorpay.com/docs/payments/test-mode/)

## 📝 Next Steps

1. **Get Production Credentials**: Sign up for live Razorpay account
2. **Update Environment**: Replace test credentials with live ones
3. **Frontend Integration**: Integrate with your actual frontend application
4. **Webhook Setup**: Configure webhooks for real-time payment updates
5. **Error Handling**: Implement comprehensive error handling
6. **Logging**: Add detailed logging for payment transactions

## 🎯 Production Checklist

- [ ] Replace test API key with live credentials
- [ ] Configure webhooks for payment notifications
- [ ] Implement proper error handling
- [ ] Add comprehensive logging
- [ ] Set up monitoring and alerts
- [ ] Test with real payment methods
- [ ] Implement rate limiting
- [ ] Add security headers
- [ ] Configure CORS properly
- [ ] Set up SSL/TLS certificates

---

**Test API Key**: `rzp_test_EnZ3V3m6bWKwsb`  
**Status**: ✅ Ready for testing  
**Last Updated**: January 2024
