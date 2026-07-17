from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.test_attempt import (
    TestAttemptCreate,
    TestAttemptResponse,
    TestAttemptUpdate,
)
from app.services import test_attempt_service

router = APIRouter(
    prefix="/test-attempts",
    tags=["Test Attempts"],
)


@router.get(
    "/",
    response_model=list[TestAttemptResponse],
)
def get_test_attempts(
    db: Session = Depends(get_db),
):
    return test_attempt_service.get_test_attempts(db)


@router.get(
    "/{attempt_id}",
    response_model=TestAttemptResponse,
)
def get_test_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = test_attempt_service.get_test_attempt(
        db,
        attempt_id,
    )

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Test Attempt not found",
        )

    return attempt


@router.post(
    "/users/{user_id}",
    response_model=TestAttemptResponse,
)
def create_test_attempt(
    user_id: int,
    attempt: TestAttemptCreate,
    db: Session = Depends(get_db),
):
    result = test_attempt_service.create_test_attempt(
        db,
        user_id,
        attempt,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User or Test not found",
        )

    return result


@router.put(
    "/{attempt_id}",
    response_model=TestAttemptResponse,
)
def update_test_attempt(
    attempt_id: int,
    attempt: TestAttemptUpdate,
    db: Session = Depends(get_db),
):
    result = test_attempt_service.update_test_attempt(
        db,
        attempt_id,
        attempt,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Test Attempt not found",
        )

    return result


@router.delete("/{attempt_id}")
def delete_test_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    deleted = test_attempt_service.delete_test_attempt(
        db,
        attempt_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Test Attempt not found",
        )

    return {
        "message": "Test Attempt deleted successfully"
    }


# ==============================
# Submit Test Attempt
# ==============================

@router.post(
    "/{attempt_id}/submit",
    response_model=TestAttemptResponse,
)
def submit_test_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = test_attempt_service.submit_test_attempt(
        db,
        attempt_id,
    )

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Test Attempt not found",
        )
