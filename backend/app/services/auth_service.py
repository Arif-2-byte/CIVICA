from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.schemas.auth import (
    LoginResponse,
    RefreshTokenResponse,
)
from app.services.session_service import (
    create_session,
    get_session_by_token,
    rotate_refresh_token,
)
from app.services.user_service import (
    authenticate_user,
    get_user_by_id,
)


# ==========================================================
# Login
# ==========================================================

def login(
    db: Session,
    *,
    username: str,
    password: str,
    device_name: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
):
    """
    Authenticate user and create login session.
    """

    user = authenticate_user(
        db,
        username,
        password,
    )

    if user is None or not user.is_active:
        return None

    access_token = create_access_token(
        {
            "sub": user.username,
            "uid": user.id,
            "role": user.role,
        }
    )

    refresh_token, _ = create_session(
        db,
        user_id=user.id,
        device_name=device_name,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )


# ==========================================================
# Refresh Token
# ==========================================================

def refresh_access_token(
    db: Session,
    *,
    refresh_token: str,
):
    """
    Validate refresh token and issue new tokens.
    """

    session = get_session_by_token(
        db,
        refresh_token,
    )

    if session is None:
        return None

    user = get_user_by_id(
        db,
        session.user_id,
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    access_token = create_access_token(
        {
            "sub": user.username,
            "uid": user.id,
            "role": user.role,
        }
    )

    new_refresh_token = rotate_refresh_token(
        db,
        session,
    )

    return RefreshTokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )