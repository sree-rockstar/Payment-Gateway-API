# 🏗️ Payment Gateway API - System Architecture

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Technology Stack](#technology-stack)
4. [Component Architecture](#component-architecture)
5. [Data Flow](#data-flow)
6. [Security Architecture](#security-architecture)
7. [Deployment Architecture](#deployment-architecture)
8. [Scalability Considerations](#scalability-considerations)
9. [Monitoring & Observability](#monitoring--observability)
10. [API Design](#api-design)

## 🎯 System Overview

The Payment Gateway API is a **microservices-based** application designed to handle user authentication, payment processing, and transaction management. The system follows a **layered architecture** pattern with clear separation of concerns.

### Core Features
- **User Authentication & Authorization** (JWT-based)
- **Payment Processing** (Razorpay integration)
- **Transaction Management** (MongoDB)
- **API Documentation** (Swagger/OpenAPI)
- **Docker Containerization**
- **Load Balancing & SSL** (Nginx)

## 🏛️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Web App   │  │  Mobile App │  │  3rd Party  │          │
│  │             │  │             │  │   Services   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTPS/HTTP
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Nginx Reverse Proxy                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Port 80   │  │  Port 443   │  │ Rate Limiting│          │
│  │   (HTTP)    │  │   (HTTPS)   │  │ & SSL/TLS   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Internal Network
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Application Layer                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Auth API  │  │ Payment API │  │  Health API │          │
│  │  (JWT)      │  │ (Razorpay)  │  │ (Monitoring)│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ Database Connection
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MongoDB Database                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Users     │  │  Payments   │  │   Sessions  │          │
│  │ Collection  │  │ Collection  │  │ Collection  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ External API
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Razorpay   │  │   Email     │  │   SMS       │          │
│  │  Gateway    │  │  Service    │  │  Service    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.9+** - Programming language
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server for production deployment

### Database
- **MongoDB 6.0** - NoSQL database for flexible data storage
- **Motor** - Async MongoDB driver for Python
- **MongoDB Compass** - Database management tool (optional)

### Authentication & Security
- **JWT (JSON Web Tokens)** - Stateless authentication
- **bcrypt** - Password hashing
- **python-jose** - JWT implementation
- **CORS** - Cross-Origin Resource Sharing

### Payment Processing
- **Razorpay** - Payment gateway integration
- **Webhook handling** - Payment verification
- **Test/Live mode** - Environment-specific configurations

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy and load balancer
- **SSL/TLS** - Secure communication

### Development & Testing
- **Swagger/OpenAPI** - API documentation
- **pytest** - Testing framework
- **curl/Postman** - API testing tools

## 🧩 Component Architecture

### 1. Application Layer (`app/`)

#### Core Components
```
app/
├── __init__.py          # Package initialization
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── database.py          # Database connection and setup
├── models.py            # Pydantic data models
├── auth.py              # Authentication utilities
├── services.py          # Business logic layer
└── routers/             # API route handlers
    ├── __init__.py
    ├── auth.py          # Authentication endpoints
    └── payments.py      # Payment processing endpoints
```

#### Key Responsibilities
- **Request/Response handling**
- **Data validation**
- **Business logic execution**
- **Error handling**
- **API documentation generation**

### 2. Database Layer

#### MongoDB Collections
```javascript
// Users Collection
{
  "_id": ObjectId,
  "email": "user@example.com",
  "full_name": "John Doe",
  "hashed_password": "bcrypt_hash",
  "created_at": ISODate,
  "updated_at": ISODate
}

// Payments Collection
{
  "_id": ObjectId,
  "order_id": "order_xxx",
  "payment_id": "pay_xxx",
  "user_id": ObjectId,
  "amount": 1000.00,
  "currency": "INR",
  "status": "pending|completed|failed",
  "description": "Payment description",
  "razorpay_data": {},
  "created_at": ISODate,
  "updated_at": ISODate
}
```

#### Database Features
- **Auto-creation** of database and collections
- **Connection pooling** for performance
- **Health monitoring** and status checks
- **Data validation** at the application level

### 3. External Integrations

#### Razorpay Integration
```python
# Payment Flow
1. Create Payment Order → Razorpay
2. Process Payment → User completes payment
3. Verify Payment → Webhook/Manual verification
4. Update Status → Database update
```

#### Security Features
- **Signature verification** for webhooks
- **Test/Live mode** separation
- **Error handling** for failed payments
- **Retry mechanisms** for network issues

## 🔄 Data Flow

### 1. User Registration Flow
```
Client → Nginx → FastAPI → Database
   ↓
1. Validate input data
2. Check if user exists
3. Hash password
4. Create user record
5. Return success response
```

### 2. User Authentication Flow
```
Client → Nginx → FastAPI → Database
   ↓
1. Validate credentials
2. Check password hash
3. Generate JWT token
4. Return token to client
```

### 3. Payment Processing Flow
```
Client → Nginx → FastAPI → Razorpay → Database
   ↓
1. Validate payment request
2. Create Razorpay order
3. Return payment details
4. Process payment (client-side)
5. Verify payment (webhook/manual)
6. Update database
```

### 4. Payment Verification Flow
```
Razorpay → FastAPI → Database
   ↓
1. Receive webhook/verification request
2. Verify signature
3. Check payment status
4. Update database
5. Return verification result
```

## 🔐 Security Architecture

### 1. Authentication & Authorization
- **JWT-based authentication**
- **Token expiration** (configurable)
- **Refresh token** mechanism (future enhancement)
- **Role-based access** control (future enhancement)

### 2. Data Security
- **Password hashing** with bcrypt
- **HTTPS/TLS** encryption
- **Input validation** and sanitization
- **SQL injection** prevention (MongoDB driver)

### 3. API Security
- **Rate limiting** (Nginx)
- **CORS configuration**
- **Request validation** (Pydantic)
- **Error handling** without information leakage

### 4. Infrastructure Security
- **Container isolation** (Docker)
- **Network segmentation** (Docker networks)
- **SSL certificates** (self-signed for dev, proper for prod)
- **Environment variables** for sensitive data

## 🚀 Deployment Architecture

### 1. Docker Container Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                     │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Nginx     │  │    API      │  │  MongoDB    │      │
│  │ Container   │  │ Container   │  │ Container   │      │
│  │ Port: 80/443│  │ Port: 8000  │  │ Port: 27017│      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   SSL       │  │   Logs      │  │   Data      │      │
│  │ Volumes     │  │ Volumes     │  │ Volumes     │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 2. Service Dependencies
```
Nginx → API → MongoDB
   ↓      ↓       ↓
SSL   Health   Data
Certs  Check   Persistence
```

### 3. Environment Configurations

#### Development Environment
- **Volume mounts** for live code changes
- **Hot reloading** enabled
- **Debug mode** active
- **Test credentials** for Razorpay

#### Production Environment
- **Optimized containers**
- **SSL certificates**
- **Rate limiting**
- **Live credentials** for Razorpay
- **Monitoring** and logging

## 📈 Scalability Considerations

### 1. Horizontal Scaling
- **Stateless API** design enables horizontal scaling
- **Load balancer** ready (Nginx)
- **Database sharding** support (MongoDB)
- **Container orchestration** ready (Kubernetes)

### 2. Performance Optimization
- **Async/await** patterns for I/O operations
- **Connection pooling** for database
- **Caching** layer (Redis - future enhancement)
- **CDN** for static assets (future enhancement)

### 3. Database Scaling
- **MongoDB replica sets** for high availability
- **Read replicas** for read-heavy workloads
- **Sharding** for large datasets
- **Indexing** strategies for query optimization

### 4. API Scaling
- **Rate limiting** per user/IP
- **Request queuing** for high load
- **Circuit breaker** patterns (future enhancement)
- **API versioning** strategy

## 📊 Monitoring & Observability

### 1. Health Checks
```python
# Health Check Endpoints
GET /health          # Basic health status
GET /db-status       # Database status and stats
```

### 2. Logging Strategy
- **Structured logging** with JSON format
- **Log levels** (DEBUG, INFO, WARNING, ERROR)
- **Request/Response logging**
- **Error tracking** and alerting

### 3. Metrics Collection
- **Request/Response times**
- **Error rates**
- **Database performance**
- **Payment success rates**

### 4. Alerting
- **Service downtime** alerts
- **High error rate** alerts
- **Database connection** issues
- **Payment processing** failures

## 🎨 API Design

### 1. RESTful Design Principles
- **Resource-based URLs**
- **HTTP method semantics**
- **Status code consistency**
- **Error response standardization**

### 2. API Versioning
```
Current: v1 (implicit)
Future: /api/v1/, /api/v2/
```

### 3. Response Format
```json
{
  "status": "success|error",
  "data": {},
  "message": "Human readable message",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 4. Error Handling
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {}
  }
}
```

## 🔧 Configuration Management

### 1. Environment Variables
```bash
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=Payment-Gateway

# Authentication
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Payment Gateway
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=your-secret

# Server
HOST=0.0.0.0
PORT=8000
```

### 2. Configuration Classes
```python
class Settings(BaseSettings):
    # Database settings
    mongodb_url: str
    database_name: str
    
    # JWT settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # Payment settings
    razorpay_key_id: str
    razorpay_key_secret: str
    
    # Server settings
    host: str
    port: int
```

## 🚀 Future Enhancements

### 1. Planned Features
- **Multi-tenant** support
- **Advanced analytics** and reporting
- **Webhook management** system
- **Payment reconciliation** tools
- **Admin dashboard** for management

### 2. Technical Improvements
- **Redis caching** layer
- **Message queue** (RabbitMQ/Redis)
- **Microservices** decomposition
- **Kubernetes** deployment
- **CI/CD pipeline** automation

### 3. Security Enhancements
- **OAuth 2.0** integration
- **Two-factor authentication**
- **Audit logging** system
- **Penetration testing** automation

---

## 📝 Architecture Decisions

### 1. Why FastAPI?
- **High performance** and async support
- **Automatic API documentation**
- **Type safety** with Pydantic
- **Modern Python** features

### 2. Why MongoDB?
- **Flexible schema** for payment data
- **Horizontal scaling** capabilities
- **JSON-like** document structure
- **Rich querying** capabilities

### 3. Why Docker?
- **Consistent environments** across development/production
- **Easy deployment** and scaling
- **Isolation** and security
- **Version control** for infrastructure

### 4. Why Razorpay?
- **Popular** in Indian market
- **Comprehensive** API documentation
- **Test environment** for development
- **Multiple payment** methods support

---

*This architecture document provides a comprehensive overview of the Payment Gateway API system design, implementation details, and future considerations.*
