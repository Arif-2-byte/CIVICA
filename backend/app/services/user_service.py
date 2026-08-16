from sqlalchemy.orm import Session

from app.auth.hashing import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


# ==========================================================
# Query Helpers
# ==========================================================

def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_username(db: Session, username: str):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def get_user_by_email(db: Session, email: str):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_all_users(db: Session):
    return (
        db.query(User)
        .order_by(User.id)
        .all()
    )


# ==========================================================
# User Creation & Authentication
# ==========================================================

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        exams=",".join(user.exams),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(
    db: Session,
    username: str,
    password: str,
):
    user = get_user_by_username(
        db,
        username,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


# ==========================================================
# Admin Operations
# ==========================================================

def update_user_role(
    db: Session,
    user_id: int,
    role: str,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    user.role = role

    db.commit()
    db.refresh(user)

    return user


def update_user_status(
    db: Session,
    user_id: int,
    is_active: bool,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    user.is_active = is_active

    db.commit()
    db.refresh(user)

    return user


def update_user_premium(
    db: Session,
    user_id: int,
    is_premium: bool,
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    user.is_premium = is_premium

    db.commit()
    db.refresh(user)

    return user