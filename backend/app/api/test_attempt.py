from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.test_attempt import (
    TestAttemptCreate,
    TestAttemptResponse,
    TestAttemptUpdate,
)
from app.services.test_attempt_service import (
    create_test_attempt,
    delete_test_attempt,
    get_test_attempt,
    get_test_attempts,
    get_user_attempts,
    submit_test_attempt,
    update_test_attempt,
)


router = APIRouter(
    prefix="/test-attempts",
    tags=["Test Attempts"],
)


@router.get(
    "/",
    response_model=list[TestAttemptResponse],
)
def read_test_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_test_attempts(db)


@router.get(
    "/my",
    response_model=list[TestAttemptResponse],
)
def read_my_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_attempts(
        db,
        current_user.id,
    )


@router.get(
    "/{attempt_id}",
    response_model=TestAttemptResponse,
)
def read_test_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempt = get_test_attempt(
        db,
        attempt_id,
    )

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    if (
        attempt.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this attempt",
        )

    return attempt


@router.post(
    "/",
    response_model=TestAttemptResponse,
)
def create_attempt(
    attempt: TestAttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    created_attempt = create_test_attempt(
        db,
        current_user.id,
        attempt,
    )

    if created_attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Test not found",
        )

    return created_attempt


@router.put(
    "/{attempt_id}",
    response_model=TestAttemptResponse,
)
def update_attempt(
    attempt_id: int,
    attempt: TestAttemptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing_attempt = get_test_attempt(
        db,
        attempt_id,
    )

    if existing_attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    if (
        existing_attempt.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this attempt",
        )

    updated_attempt = update_test_attempt(
        db,
        attempt_id,
        attempt,
    )

    return updated_attempt


@router.post(
    "/{attempt_id}/submit",
    response_model=TestAttemptResponse,
)
def submit_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_attempt = get_test_attempt(
        db,
        attempt_id,
    )

    if existing_attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    if (
        existing_attempt.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this attempt",
        )

    submitted_attempt = submit_test_attempt(
        db,
        attempt_id,
    )

    return submitted_attempt


@router.delete(
    "/{attempt_id}",
)
def delete_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_attempt = get_test_attempt(
        db,
        attempt_id,
    )

    if existing_attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    if (
        existing_attempt.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this attempt",
        )

    deleted = delete_test_attempt(
        db,
        attempt_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    return {
        "message": "Test attempt deleted successfully"
    }