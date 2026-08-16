from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserPremiumUpdate,
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate,
)
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user_premium,
    update_user_role,
    update_user_status,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# ==========================================================
# Admin APIs
# ==========================================================

@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
def change_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = update_user_role(
        db,
        user_id,
        payload.role,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def change_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = update_user_status(
        db,
        user_id,
        payload.is_active,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.patch(
    "/{user_id}/premium",
    response_model=UserResponse,
)
def change_premium(
    user_id: int,
    payload: UserPremiumUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = update_user_premium(
        db,
        user_id,
        payload.is_premium,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user