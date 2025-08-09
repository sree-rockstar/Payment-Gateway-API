# Payment Gateway API

A FastAPI backend application with user authentication, session handling, and payment gateway integration using MongoDB and Razorpay.

## 🚀 Features

- **User Authentication**: Sign up, sign in, and sign out with JWT tokens
- **Session Handling**: Protected routes with JWT-based authentication
- **Payment Gateway**: Razorpay integration for payment processing
- **Database**: MongoDB for data persistence
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## 📋 Prerequisites

- Python 3.8+
- MongoDB (running on localhost:27017)
- Razorpay account (for payment processing)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB (running on localhost:27017)
- Git

### One-Command Setup & Run
```bash
# Clone and setup
git clone <repository-url>
cd Payment-Gateway-API

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file (if not exists)
cp env.example .env

# Start the application
python run.py
```

The API will be available at `http://localhost:8001` (or the port specified in your .env file)

## 🛠️ Detailed Installation

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Payment-Gateway-API
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy environment file
cp env.example .env
```

Edit `.env` file with your configuration:
```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=Payment-Gateway

# JWT Configuration
SECRET_KEY=your-secret-key-here-make-it-long-and-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Razorpay Configuration (Test Mode)
RAZORPAY_KEY_ID=rzp_test_EnZ3V3m6bWKwsb
RAZORPAY_KEY_SECRET=your-razorpay-test-key-secret

# Server Configuration
HOST=0.0.0.0
PORT=8001
```

### Step 5: Start MongoDB
```bash
# Make sure MongoDB is running on localhost:27017
mongod
```

**Note**: The application will automatically:
- ✅ Check if MongoDB is running
- ✅ Connect to the database
- ✅ Create the database if it doesn't exist
- ✅ Create required collections (users, payments) if they don't exist
- ✅ Provide detailed status messages during startup

### Step 6: Run the Application
```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the application
python run.py
```

### Step 7: Verify Installation
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health
- **Alternative Docs**: http://localhost:8001/redoc

## 🖥️ Terminal Commands Reference

### Development Commands
```bash
# Start the server
python run.py

# Start with auto-reload (default)
python run.py

# Test database connection
python test_db_connection.py

# Run tests
python test_razorpay.py
python test_api.py

# Check server status
curl http://localhost:8001/health

# Check database status
curl http://localhost:8001/db-status
```

### Virtual Environment Management
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate virtual environment
deactivate

# Install dependencies
pip install -r requirements.txt

# Update pip
pip install --upgrade pip
```

### MongoDB Commands
```bash
# Start MongoDB
mongod

# Check MongoDB status
mongo --eval "db.runCommand('ping')"

# Connect to MongoDB shell
mongo
```

### Port Management
```bash
# Check what's running on port 8001
lsof -i :8001

# Kill process on specific port
kill -9 $(lsof -t -i:8001)

# Change port in .env file
sed -i '' 's/PORT=8001/PORT=8002/' .env
```

## 📚 API Documentation

The API includes comprehensive Swagger/OpenAPI documentation with interactive features:

### Documentation URLs
- **Swagger UI**: http://localhost:8001/docs - Interactive API documentation with "Try it out" feature
- **ReDoc**: http://localhost:8001/redoc - Alternative documentation view
- **OpenAPI JSON**: http://localhost:8001/openapi.json - Raw OpenAPI specification
- **Root Page**: http://localhost:8001/ - API overview and quick links

### Swagger Features
- ✅ **Interactive Testing**: Try endpoints directly from the documentation
- ✅ **JWT Authentication**: Built-in authorization support
- ✅ **Request/Response Examples**: Pre-filled examples for all endpoints
- ✅ **Data Model Documentation**: Complete schema documentation
- ✅ **Error Response Documentation**: Detailed error examples
- ✅ **External Documentation Links**: Links to JWT and Razorpay docs
- ✅ **Multiple Server Support**: Development and production server configurations

### Using Swagger UI
1. **Get JWT Token**: Use `/auth/signin` endpoint to get a token
2. **Authorize**: Click the "Authorize" button in Swagger UI
3. **Enter Token**: Use format `Bearer <your-jwt-token>`
4. **Test Endpoints**: Use "Try it out" feature to test protected endpoints

## 🔐 Authentication Endpoints

### Sign Up
```http
POST http://localhost:8001/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```

### Sign In
```http
POST http://localhost:8001/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### Get Profile (Protected)
```http
GET http://localhost:8001/auth/profile
Authorization: Bearer <your-jwt-token>
```

### Sign Out
```http
POST http://localhost:8001/auth/signout
Authorization: Bearer <your-jwt-token>
```

## 💳 Payment Endpoints

### Create Payment (Protected)
```http
POST http://localhost:8001/payments/create-payment
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "amount": 1000.00,
  "currency": "INR",
  "description": "Payment for services"
}
```

### Verify Payment (Protected)
```http
POST http://localhost:8001/payments/verify-payment
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "razorpay_payment_id": "pay_xxx",
  "razorpay_order_id": "order_xxx",
  "razorpay_signature": "signature_xxx"
}
```

### Get My Payments (Protected)
```http
GET http://localhost:8001/payments/my-payments
Authorization: Bearer <your-jwt-token>
```

## 🗄️ Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "full_name": "John Doe",
  "hashed_password": "hashed_password_string",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

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
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `Payment-Gateway` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `RAZORPAY_KEY_ID` | Razorpay key ID | `rzp_test_EnZ3V3m6bWKwsb` |
| `RAZORPAY_KEY_SECRET` | Razorpay key secret | `your-razorpay-test-key-secret` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Razorpay Setup

1. **Get your Razorpay credentials**:
   - Sign up at [Razorpay Dashboard](https://dashboard.razorpay.com)
   - Go to Settings → API Keys
   - Copy your Key ID and Key Secret

2. **Update environment variables**:
   ```bash
   # Edit .env file
   RAZORPAY_KEY_ID=your_actual_key_id
   RAZORPAY_KEY_SECRET=your_actual_key_secret
   ```

3. **Test Mode vs Live Mode**:
   - Use test credentials for development
   - Switch to live credentials for production
   - Test API Key: `rzp_test_EnZ3V3m6bWKwsb` (already configured)

## 🧪 Testing

### Razorpay Integration Testing

The application is configured with Razorpay test credentials:
- **Test API Key**: `rzp_test_EnZ3V3m6bWKwsb`
- **Test Mode**: Enabled

#### Quick Test Script
Run the comprehensive Razorpay test script:
```bash
python test_razorpay.py
```

This script will:
- Create a test user
- Authenticate and get JWT token
- Test payment creation with Razorpay
- Verify payment records in database
- Test all protected endpoints

#### Test Card Details (for frontend integration)
- **Card Number**: 4111 1111 1111 1111
- **Expiry**: Any future date
- **CVV**: Any 3 digits
- **Name**: Any name

### Swagger Testing

Test the API using the interactive Swagger documentation:

```bash
# Start the server
python3 run.py

# Test Swagger integration
python3 test_swagger.py
```

Then visit http://localhost:8001/docs to:
- View interactive API documentation
- Test endpoints directly from the browser
- Use the "Try it out" feature
- Authorize with JWT tokens

### Manual Testing

You can also test the API using curl or any HTTP client:

1. **Sign up a new user**
   ```bash
   curl -X POST "http://localhost:8001/auth/signup" \
        -H "Content-Type: application/json" \
        -d '{"email":"test@example.com","full_name":"Test User","password":"password123"}'
   ```

2. **Sign in to get token**
   ```bash
   curl -X POST "http://localhost:8001/auth/signin" \
        -H "Content-Type: application/json" \
        -d '{"email":"test@example.com","password":"password123"}'
   ```

3. **Create a payment**
   ```bash
   curl -X POST "http://localhost:8001/payments/create-payment" \
        -H "Authorization: Bearer YOUR_JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"amount":1000.00,"currency":"INR","description":"Test payment"}'
   ```

## 🚨 Security Notes

- Change the default `SECRET_KEY` in production
- Use strong passwords
- Configure CORS properly for production
- Use HTTPS in production
- Store sensitive data securely
- Implement rate limiting for production use

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support, please open an issue in the repository or contact the development team.