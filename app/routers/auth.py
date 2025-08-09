from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List
from ..models import UserCreate, UserLogin, UserResponse, Token
from ..services import UserService
from ..auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user account",
    description="""
    Create a new user account with email and password.

    The password will be securely hashed using bcrypt before storage.
    Email must be unique and valid format.

    **Example Usage:**
    ```bash
    curl -X POST "http://localhost:8000/auth/signup" \\
         -H "Content-Type: application/json" \\
         -d '{
           "email": "user@example.com",
           "password": "securepassword123",
           "full_name": "John Doe"
         }'
    ```
    """,
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "507f1f77bcf86cd799439011",
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Bad request - validation error or email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered"
                    }
                }
            }
        }
    }
)
async def signup(user_data: UserCreate):
    """Create a new user account."""
    user_service = UserService()
    return await user_service.create_user(user_data)


@router.post(
    "/signin",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Sign in user and get JWT token",
    description="""
    Authenticate user with email and password, return JWT token.

    The returned access token should be used in the Authorization header
    for protected endpoints: `Authorization: Bearer <token>`

    **Example Usage:**
    ```bash
    curl -X POST "http://localhost:8000/auth/signin" \\
         -H "Content-Type: application/json" \\
         -d '{
           "email": "user@example.com",
           "password": "securepassword123"
         }'
    ```
    """,
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid email or password"
                    }
                }
            }
        }
    }
)
async def signin(user_credentials: UserLogin):
    """Sign in user and return JWT token."""
    user_service = UserService()
    token = await user_service.authenticate_user(
        user_credentials.email, user_credentials.password
    )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/profile",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="""
    Get the profile information of the currently authenticated user.

    Requires a valid JWT token in the Authorization header.

    **Example Usage:**
    ```bash
    curl -X GET "http://localhost:8000/auth/profile" \\
         -H "Authorization: Bearer YOUR_JWT_TOKEN"
    ```
    """,
    responses={
        200: {
            "description": "User profile retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "507f1f77bcf86cd799439011",
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
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
        }
    },
    dependencies=[Depends(security)]
)
async def get_profile(current_user_email: str = Depends(get_current_user)):
    """Get current user profile."""
    user_service = UserService()
    user = await user_service.get_user_by_email(current_user_email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.post(
    "/signout",
    status_code=status.HTTP_200_OK,
    summary="Sign out user",
    description="""
    Sign out the current user.

    Note: JWT tokens are stateless, so this endpoint simply returns success.
    The client should discard the token and not use it for future requests.

    **Example Usage:**
    ```bash
    curl -X POST "http://localhost:8000/auth/signout" \\
         -H "Authorization: Bearer YOUR_JWT_TOKEN"
    ```
    """,
    responses={
        200: {
            "description": "Successfully signed out",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Successfully signed out"
                    }
                }
            }
        },
        401: {
            "description": "Invalid or missing authentication token"
        }
    },
    dependencies=[Depends(security)]
)
async def signout():
    """Sign out user (client should discard token)."""
    # JWT tokens are stateless, so we just return success
    # The client should discard the token
    return {"message": "Successfully signed out"}
