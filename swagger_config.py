"""
Swagger/OpenAPI Configuration for Payment Gateway API
"""

# Swagger UI Configuration
SWAGGER_UI_CONFIG = {
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
}

# OpenAPI Tags Configuration
OPENAPI_TAGS = [
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

# Security Schemes Configuration
SECURITY_SCHEMES = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token obtained from /auth/signin endpoint"
    }
}

# Server Configuration
SERVERS = [
    {
        "url": "http://localhost:8000",
        "description": "Development server"
    },
    {
        "url": "https://api.example.com",
        "description": "Production server"
    }
]

# Contact Information
CONTACT_INFO = {
    "name": "Payment Gateway API Support",
    "email": "support@example.com",
    "url": "https://github.com/your-repo/payment-gateway-api"
}

# License Information
LICENSE_INFO = {
    "name": "MIT",
    "url": "https://opensource.org/licenses/MIT"
}
