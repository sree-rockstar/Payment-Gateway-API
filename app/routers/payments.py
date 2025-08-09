from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List
from ..models import PaymentCreate, PaymentResponse, PaymentVerification
from ..services import PaymentService
from ..auth import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])
security = HTTPBearer()


@router.post(
    "/create-payment",
    summary="Create a new payment order",
    description="""
    Create a new payment order with Razorpay integration.
    
    This endpoint creates a payment order in Razorpay and stores the payment
    record in the database. The returned order ID should be used with the
    Razorpay checkout to process the payment.
    
    **Payment Flow:**
    1. Call this endpoint to create payment order
    2. Use the returned `razorpay_order_id` with Razorpay checkout
    3. After payment completion, call `/verify-payment` endpoint
    
    **Example Usage:**
    ```bash
    curl -X POST "http://localhost:8000/payments/create-payment" \\
         -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
         -H "Content-Type: application/json" \\
         -d '{"amount":1000,"currency":"INR","description":"Test payment"}'
    ```
    """,
    responses={
        200: {
            "description": "Payment order created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "payment_id": "507f1f77bcf86cd799439011",
                        "order_id": "order_1234567890",
                        "amount": 1000.0,
                        "currency": "INR",
                        "razorpay_order_id": "order_rzp_1234567890"
                    }
                }
            }
        },
        401: {
            "description": "Invalid or missing authentication token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not validate credentials"
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found"
                    }
                }
            }
        },
        500: {
            "description": "Payment creation failed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Failed to create payment order: Invalid API key"
                    }
                }
            }
        }
    },
    dependencies=[Depends(security)]
)
async def create_payment(
    payment_data: PaymentCreate,
    current_user_email: str = Depends(get_current_user)
):
    """Create a new payment order."""
    payment_service = PaymentService()
    return await payment_service.create_payment(payment_data, current_user_email)


@router.post(
    "/verify-payment", 
    response_model=PaymentResponse,
    summary="Verify payment and update status",
    description="""
    Verify a completed payment with Razorpay and update the payment status.
    
    This endpoint should be called after a payment is completed through the
    Razorpay checkout. It verifies the payment signature and updates the
    payment status in the database.
    
    **Required Parameters:**
    - `razorpay_payment_id`: Payment ID from Razorpay
    - `razorpay_order_id`: Order ID from Razorpay
    - `razorpay_signature`: Payment signature from Razorpay
    
    **Example Usage:**
    ```bash
    curl -X POST "http://localhost:8000/payments/verify-payment" \\
         -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
         -H "Content-Type: application/json" \\
         -d '{
           "razorpay_payment_id": "pay_1234567890",
           "razorpay_order_id": "order_1234567890",
           "razorpay_signature": "signature_1234567890"
         }'
    ```
    """,
    responses={
        200: {
            "description": "Payment verified successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "507f1f77bcf86cd799439011",
                        "order_id": "order_1234567890",
                        "amount": 1000.00,
                        "currency": "INR",
                        "status": "completed",
                        "user_id": "507f1f77bcf86cd799439012",
                        "description": "Payment for services",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Invalid payment signature or data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid payment signature"
                    }
                }
            }
        },
        401: {
            "description": "Invalid or missing authentication token"
        },
        404: {
            "description": "Payment or user not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Payment not found"
                    }
                }
            }
        }
    },
    dependencies=[Depends(security)]
)
async def verify_payment(
    verification_data: PaymentVerification,
    current_user_email: str = Depends(get_current_user)
):
    """Verify payment and update status."""
    payment_service = PaymentService()
    return await payment_service.verify_payment(verification_data, current_user_email)


@router.get(
    "/my-payments", 
    response_model=List[PaymentResponse],
    summary="Get all payments for the current user",
    description="""
    Retrieve all payment records for the currently authenticated user.
    
    Returns a list of all payments (pending, completed, failed) associated
    with the user's account, ordered by creation date (newest first).
    
    **Example Usage:**
    ```bash
    curl -X GET "http://localhost:8000/payments/my-payments" \\
         -H "Authorization: Bearer YOUR_JWT_TOKEN"
    ```
    """,
    responses={
        200: {
            "description": "List of user payments retrieved successfully",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "507f1f77bcf86cd799439011",
                            "order_id": "order_1234567890",
                            "amount": 1000.00,
                            "currency": "INR",
                            "status": "completed",
                            "user_id": "507f1f77bcf86cd799439012",
                            "description": "Payment for services",
                            "created_at": "2024-01-01T00:00:00Z",
                            "updated_at": "2024-01-01T00:00:00Z"
                        },
                        {
                            "id": "507f1f77bcf86cd799439013",
                            "order_id": "order_0987654321",
                            "amount": 500.00,
                            "currency": "INR",
                            "status": "pending",
                            "user_id": "507f1f77bcf86cd799439012",
                            "description": "Another payment",
                            "created_at": "2024-01-01T01:00:00Z",
                            "updated_at": "2024-01-01T01:00:00Z"
                        }
                    ]
                }
            }
        },
        401: {
            "description": "Invalid or missing authentication token"
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found"
                    }
                }
            }
        }
    },
    dependencies=[Depends(security)]
)
async def get_my_payments(current_user_email: str = Depends(get_current_user)):
    """Get all payments for the current user."""
    payment_service = PaymentService()
    return await payment_service.get_user_payments(current_user_email)
