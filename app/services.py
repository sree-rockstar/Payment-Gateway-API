from datetime import datetime
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException, status
from .database import get_database
from .models import UserCreate, UserResponse, PaymentCreate, PaymentResponse, PaymentStatus
from .auth import get_password_hash, verify_password, create_access_token
import razorpay


class UserService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        hashed_password = get_password_hash(user_data.password)
        user_doc = {
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(user_doc)
        user_doc["id"] = str(result.inserted_id)
        
        return UserResponse(**user_doc)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token."""
        user = await self.collection.find_one({"email": email})
        if not user:
            return None
        
        if not verify_password(password, user["hashed_password"]):
            return None
        
        # Create access token
        access_token = create_access_token(data={"sub": user["email"]})
        return access_token
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email."""
        user = await self.collection.find_one({"email": email})
        if not user:
            return None
        
        user["id"] = str(user["_id"])
        return UserResponse(**user)


class PaymentService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.payments
        # Initialize Razorpay client
        self.razorpay_client = razorpay.Client(
            auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
        )
    
    async def create_payment(self, payment_data: PaymentCreate, user_email: str) -> dict:
        """Create a new payment order."""
        # Get user ID
        user_service = UserService()
        user = await user_service.get_user_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create Razorpay order
        order_data = {
            "amount": int(payment_data.amount * 100),  # Convert to paise
            "currency": payment_data.currency,
            "receipt": f"receipt_{datetime.utcnow().timestamp()}",
            "notes": {
                "description": payment_data.description or "Payment for services"
            }
        }
        
        try:
            razorpay_order = self.razorpay_client.order.create(data=order_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create payment order: {str(e)}"
            )
        
        # Save payment record to database
        payment_doc = {
            "order_id": razorpay_order["id"],
            "amount": payment_data.amount,
            "currency": payment_data.currency,
            "status": PaymentStatus.PENDING,
            "user_id": user.id,
            "description": payment_data.description,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(payment_doc)
        payment_doc["id"] = str(result.inserted_id)
        
        return {
            "payment_id": payment_doc["id"],
            "order_id": razorpay_order["id"],
            "amount": payment_data.amount,
            "currency": payment_data.currency,
            "razorpay_order_id": razorpay_order["id"]
        }
    
    async def verify_payment(self, verification_data, user_email: str) -> PaymentResponse:
        """Verify payment and update status."""
        # Get user ID
        user_service = UserService()
        user = await user_service.get_user_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Find payment record
        payment = await self.collection.find_one({
            "order_id": verification_data.razorpay_order_id,
            "user_id": user.id
        })
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        # Verify signature
        try:
            self.razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": verification_data.razorpay_order_id,
                "razorpay_payment_id": verification_data.razorpay_payment_id,
                "razorpay_signature": verification_data.razorpay_signature
            })
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payment signature"
            )
        
        # Update payment status
        update_data = {
            "status": PaymentStatus.COMPLETED,
            "updated_at": datetime.utcnow(),
            "razorpay_payment_id": verification_data.razorpay_payment_id
        }
        
        await self.collection.update_one(
            {"_id": payment["_id"]},
            {"$set": update_data}
        )
        
        payment.update(update_data)
        payment["id"] = str(payment["_id"])
        
        return PaymentResponse(**payment)
    
    async def get_user_payments(self, user_email: str) -> list[PaymentResponse]:
        """Get all payments for a user."""
        user_service = UserService()
        user = await user_service.get_user_by_email(user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        payments = []
        async for payment in self.collection.find({"user_id": user.id}):
            payment["id"] = str(payment["_id"])
            payments.append(PaymentResponse(**payment))
        
        return payments


# Import settings at the end to avoid circular import
from .config import settings
