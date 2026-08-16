import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.session import Session as UserSession


# ==========================================================
# Token Helpers
# ==========================================================

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


# ==========================================================
# Session Operations
# ==========================================================

def create_session(
    db: Session,
    *,
    user_id: int,
    device_name: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
):
    """
    Create a new login session.
    """

    refresh_token = generate_refresh_token()

    session = UserSession(
        user_id=user_id,
        token_hash=hash_refresh_token(refresh_token),
        device_name=device_name,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return refresh_token, session


def get_session_by_token(
    db: Session,
    refresh_token: str,
):
    """
    Return a valid session using the refresh token.
    """

    token_hash = hash_refresh_token(refresh_token)

    session = (
        db.query(UserSession)
        .filter(
            UserSession.token_hash == token_hash,
            UserSession.is_revoked.is_(False),
        )
        .first()
    )

    if session is None:
        return None

    if session.expires_at <= datetime.now(timezone.utc):
        session.is_revoked = True
        db.commit()
        return None

    return session


def rotate_refresh_token(
    db: Session,
    session: UserSession,
):
    """
    Rotate refresh token after successful refresh.
    """

    new_refresh_token = generate_refresh_token()

    session.token_hash = hash_refresh_token(new_refresh_token)
    session.last_used_at = datetime.now(timezone.utc)
    session.expires_at = (
        datetime.now(timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    db.commit()
    db.refresh(session)

    return new_refresh_token


def revoke_session(
    db: Session,
    session: UserSession,
):
    session.is_revoked = True
    db.commit()


def revoke_all_sessions(
    db: Session,
    user_id: int,
):
    (
        db.query(UserSession)
        .filter(
            UserSession.user_id == user_id,
            UserSession.is_revoked.is_(False),
        )
        .update(
            {
                UserSession.is_revoked: True,
            },
            synchronize_session=False,
        )
    )

    db.commit()


def touch_session(
    db: Session,
    session: UserSession,
):
    session.last_used_at = datetime.now(timezone.utc)
    db.commit()


def delete_expired_sessions(
    db: Session,
):
    (
        db.query(UserSession)
        .filter(
            UserSession.expires_at
            < datetime.now(timezone.utc)
        )
        .delete(
            synchronize_session=False,
        )
    )

    db.commit()