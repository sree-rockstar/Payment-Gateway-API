from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, FileResponse
from .database import connect_to_mongo, close_mongo_connection
from .routers import auth, payments
import os

# Custom OpenAPI configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Payment Gateway API",
        version="1.0.0",
        description="""
# 🚀 Payment Gateway API

A comprehensive FastAPI backend application with user authentication, session handling, and payment gateway integration using MongoDB and Razorpay.

## 🔑 Features

* **User Authentication**: Sign up, sign in, and sign out with JWT tokens
* **Session Handling**: Protected routes with JWT-based authentication
* **Payment Gateway**: Razorpay integration for payment processing
* **Database**: MongoDB for data persistence
* **Security**: bcrypt password hashing and JWT token validation

## 🛠️ Technology Stack

* **Backend**: FastAPI (Python)
* **Database**: MongoDB with Motor (async)
* **Authentication**: JWT with python-jose
* **Payment Gateway**: Razorpay
* **Password Hashing**: bcrypt
* **Documentation**: Swagger/OpenAPI

## 📋 Prerequisites

* Python 3.8+
* MongoDB (running on localhost:27017)
* Razorpay account (for payment processing)

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `Payment-Gateway` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |
| `RAZORPAY_KEY_ID` | Razorpay key ID | `rzp_test_EnZ3V3m6bWKwsb` |
| `RAZORPAY_KEY_SECRET` | Razorpay key secret | `your-razorpay-test-key-secret` |

## 🧪 Testing

### Test Card Details (for frontend integration)
* **Card Number**: 4111 1111 1111 1111
* **Expiry**: Any future date
* **CVV**: Any 3 digits
* **Name**: Any name

### Quick Test Script
```bash
python3 test_razorpay.py
```

## 📚 API Documentation

* **Swagger UI**: `/docs` - Interactive API documentation
* **ReDoc**: `/redoc` - Alternative documentation view
* **OpenAPI JSON**: `/openapi.json` - Raw OpenAPI specification

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## 💳 Payment Flow

1. **Create Payment**: POST `/payments/create-payment`
2. **Process Payment**: Use Razorpay checkout
3. **Verify Payment**: POST `/payments/verify-payment`
4. **Check Status**: GET `/payments/my-payments`

## 🚨 Security Notes

* Change the default `SECRET_KEY` in production
* Use strong passwords
* Configure CORS properly for production
* Use HTTPS in production
* Store sensitive data securely

## 📞 Support

For support, please open an issue in the repository or contact the development team.
        """,
        routes=app.routes,
    )
    
    # Custom tags for better organization
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and session management endpoints. Includes sign up, sign in, sign out, and profile management.",
            "externalDocs": {
                "description": "JWT Authentication Guide",
                "url": "https://jwt.io/introduction",
            },
        },
        {
            "name": "Payments",
            "description": "Payment processing endpoints with Razorpay integration. Create payments, verify transactions, and manage payment records.",
            "externalDocs": {
                "description": "Razorpay API Documentation",
                "url": "https://razorpay.com/docs/api/understand/",
            },
        },
        {
            "name": "Health",
            "description": "System health and status endpoints for monitoring and debugging.",
        },
    ]
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /auth/signin endpoint"
        }
    }
    
    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server"
        }
    ]
    
    # Add contact information
    openapi_schema["info"]["contact"] = {
        "name": "Payment Gateway API Support",
        "email": "support@example.com",
        "url": "https://github.com/your-repo/payment-gateway-api"
    }
    
    # Add license information
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Fix security requirements for protected endpoints
    protected_paths = [
        "/auth/profile",
        "/auth/signout", 
        "/payments/create-payment",
        "/payments/verify-payment",
        "/payments/my-payments"
    ]
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                endpoint = openapi_schema["paths"][path][method]
                # Set security requirement for protected endpoints
                if path in protected_paths:
                    endpoint["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Create FastAPI app with enhanced metadata
app = FastAPI(
    title="Payment Gateway API",
    description="A comprehensive FastAPI backend with user authentication and payment gateway integration",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 3,
        "displayRequestDuration": True,
        "docExpansion": "list",
        "filter": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "syntaxHighlight.theme": "monokai",
        "tryItOutEnabled": True,
        "persistAuthorization": True,
        "displayOperationId": False,
        "deepLinking": True,
        "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
        "validatorUrl": None,
        "oauth2RedirectUrl": None,
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "showMutatedRequest": True,
        "initOAuth": {
            "clientId": "your-client-id",
            "clientSecret": "your-client-secret",
            "realm": "your-realm",
            "appName": "Payment Gateway API",
            "scopes": "read write",
            "additionalQueryStringParams": {},
            "useBasicAuthenticationWithAccessCodeGrant": False,
            "usePkceWithAuthorizationCodeGrant": False
        }
    }
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routers
app.include_router(auth.router)
app.include_router(payments.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Gateway API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; }
            .card { background: #f9f9f9; padding: 20px; margin: 10px 0; border-radius: 5px; }
            .endpoint { background: #e3f2fd; padding: 15px; margin: 5px 0; border-radius: 3px; }
            .auth { background: #fff3e0; }
            .payment { background: #e8f5e8; }
            .health { background: #f3e5f5; }
            a { color: #1976d2; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 Payment Gateway API</h1>
            <p>FastAPI backend with authentication and Razorpay integration</p>
        </div>
        
        <div class="card">
            <h2>📚 Documentation</h2>
            <div class="endpoint">
                <strong>Swagger UI:</strong> <a href="/docs">/docs</a> - Interactive API documentation
            </div>
            <div class="endpoint">
                <strong>ReDoc:</strong> <a href="/redoc">/redoc</a> - Alternative documentation view
            </div>
            <div class="endpoint">
                <strong>OpenAPI JSON:</strong> <a href="/openapi.json">/openapi.json</a> - Raw specification
            </div>
        </div>
        
        <div class="card">
            <h2>🔐 Authentication Endpoints</h2>
            <div class="endpoint auth">
                <strong>POST /auth/signup</strong> - Create new user account
            </div>
            <div class="endpoint auth">
                <strong>POST /auth/signin</strong> - Login and get JWT token
            </div>
            <div class="endpoint auth">
                <strong>GET /auth/profile</strong> - Get user profile (protected)
            </div>
            <div class="endpoint auth">
                <strong>POST /auth/signout</strong> - Sign out
            </div>
        </div>
        
        <div class="card">
            <h2>💳 Payment Endpoints</h2>
            <div class="endpoint payment">
                <strong>POST /payments/create-payment</strong> - Create payment order (protected)
            </div>
            <div class="endpoint payment">
                <strong>POST /payments/verify-payment</strong> - Verify payment (protected)
            </div>
            <div class="endpoint payment">
                <strong>GET /payments/my-payments</strong> - Get user payments (protected)
            </div>
        </div>
        
        <div class="card">
            <h2>🔧 System Endpoints</h2>
            <div class="endpoint health">
                <strong>GET /health</strong> - Health check
            </div>
            <div class="endpoint health">
                <strong>GET /db-status</strong> - Database status and statistics
            </div>
        </div>
        
        <div class="card">
            <h2>🧪 Testing</h2>
            <p><strong>Test Script:</strong> <code>python3 test_razorpay.py</code></p>
            <p><strong>Frontend Test:</strong> <a href="/test_frontend.html">test_frontend.html</a></p>
            <p><strong>Test API Key:</strong> <code>rzp_test_EnZ3V3m6bWKwsb</code></p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    from .database import test_connection
    
    db_status = await test_connection()
    
    return {
        "status": "healthy" if db_status["status"] == "connected" else "unhealthy",
        "service": "Payment Gateway API",
        "version": "1.0.0",
        "database": db_status,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/db-status")
async def database_status():
    """Database status endpoint for detailed database information."""
    from .database import test_connection, db
    from .config import settings
    
    db_status = await test_connection()
    
    if db_status["status"] == "connected":
        try:
            # Get database info
            collections = await db.database.list_collection_names()
            db_info = await db.database.command("dbStats")
            
            return {
                "status": "connected",
                "database_name": settings.database_name,
                "collections": collections,
                "database_stats": {
                    "collections": db_info.get("collections", 0),
                    "data_size": db_info.get("dataSize", 0),
                    "storage_size": db_info.get("storageSize", 0),
                    "indexes": db_info.get("indexes", 0)
                },
                "connection_url": settings.mongodb_url
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "database_name": settings.database_name
            }
    else:
        return db_status

@app.get("/test_frontend.html", response_class=HTMLResponse)
async def test_frontend():
    """Serve the test frontend HTML file."""
    try:
        with open("test_frontend.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Test Frontend Not Found</h1><p>The test_frontend.html file is not available.</p>",
            status_code=404
        )

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )

# Custom ReDoc
@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
    )
