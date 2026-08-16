from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.schemas.auth import (
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
)
from app.services.auth_service import (
    login as login_user,
    refresh_access_token,
)
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# Test Endpoint
# ==========================================================

@router.get("/test")
def test_auth():
    return {
        "message": "Authentication API Working!"
    }


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    return create_user(db, user)


# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    result = login_user(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return result


# ==========================================================
# Refresh Token
# ==========================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token using a valid refresh token.
    """

    result = refresh_access_token(
        db=db,
        refresh_token=request.refresh_token,
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token.",
        )

    return result


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user=Depends(get_current_user),
):
    """
    Return the currently authenticated user.
    """
    return current_user