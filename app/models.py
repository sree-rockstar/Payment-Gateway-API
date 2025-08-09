from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class UserBase(BaseModel):
    """Base user model with common fields."""
    email: EmailStr = Field(
        ..., 
        description="User's email address (must be unique)",
        example="user@example.com"
    )
    full_name: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="User's full name",
        example="John Doe"
    )


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(
        ..., 
        min_length=6,
        description="User's password (minimum 6 characters)",
        example="securepassword123"
    )


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr = Field(
        ..., 
        description="User's email address",
        example="user@example.com"
    )
    password: str = Field(
        ..., 
        description="User's password",
        example="securepassword123"
    )


class UserResponse(UserBase):
    """User response model."""
    id: str = Field(
        ..., 
        description="Unique user identifier",
        example="507f1f77bcf86cd799439011"
    )
    created_at: datetime = Field(
        ..., 
        description="User creation timestamp",
        example="2024-01-01T00:00:00Z"
    )
    updated_at: datetime = Field(
        ..., 
        description="User last update timestamp",
        example="2024-01-01T00:00:00Z"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "full_name": "John Doe",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class Token(BaseModel):
    """JWT token response model."""
    access_token: str = Field(
        ..., 
        description="JWT access token for authentication",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA0MDY0MDAwfQ.example_signature"
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')",
        example="bearer"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzA0MDY0MDAwfQ.example_signature",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Token data model for JWT payload."""
    email: Optional[str] = Field(
        None, 
        description="User email from JWT token",
        example="user@example.com"
    )


class PaymentCreate(BaseModel):
    """Payment creation model."""
    amount: float = Field(
        ..., 
        gt=0,
        description="Payment amount (must be greater than 0)",
        example=1000.00
    )
    currency: str = Field(
        default="INR", 
        max_length=3,
        description="Payment currency (3-letter code)",
        example="INR"
    )
    description: Optional[str] = Field(
        None,
        description="Payment description (optional)",
        example="Payment for services"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 1000.00,
                "currency": "INR",
                "description": "Payment for services"
            }
        }


class PaymentResponse(BaseModel):
    """Payment response model."""
    id: str = Field(
        ..., 
        description="Unique payment identifier",
        example="507f1f77bcf86cd799439011"
    )
    order_id: str = Field(
        ..., 
        description="Razorpay order ID",
        example="order_1234567890"
    )
    amount: float = Field(
        ..., 
        description="Payment amount",
        example=1000.00
    )
    currency: str = Field(
        ..., 
        description="Payment currency",
        example="INR"
    )
    status: PaymentStatus = Field(
        ..., 
        description="Payment status",
        example="completed"
    )
    user_id: str = Field(
        ..., 
        description="User ID who made the payment",
        example="507f1f77bcf86cd799439012"
    )
    description: Optional[str] = Field(
        None,
        description="Payment description",
        example="Payment for services"
    )
    created_at: datetime = Field(
        ..., 
        description="Payment creation timestamp",
        example="2024-01-01T00:00:00Z"
    )
    updated_at: datetime = Field(
        ..., 
        description="Payment last update timestamp",
        example="2024-01-01T00:00:00Z"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
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


class PaymentVerification(BaseModel):
    """Payment verification model."""
    razorpay_payment_id: str = Field(
        ..., 
        description="Payment ID from Razorpay",
        example="pay_1234567890"
    )
    razorpay_order_id: str = Field(
        ..., 
        description="Order ID from Razorpay",
        example="order_1234567890"
    )
    razorpay_signature: str = Field(
        ..., 
        description="Payment signature from Razorpay",
        example="signature_1234567890"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "razorpay_payment_id": "pay_1234567890",
                "razorpay_order_id": "order_1234567890",
                "razorpay_signature": "signature_1234567890"
            }
        }
