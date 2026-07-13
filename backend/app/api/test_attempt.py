from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
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
    update_test_attempt,
)

router = APIRouter(
    prefix="/test-attempts",
    tags=["Test Attempts"],
)


@router.get("/", response_model=list[TestAttemptResponse])
def read_test_attempts(
    db: Session = Depends(get_db),
):
    return get_test_attempts(db)


@router.get("/{attempt_id}", response_model=TestAttemptResponse)
def read_test_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
    attempt = get_test_attempt(db, attempt_id)

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    return attempt


@router.post("/{user_id}", response_model=TestAttemptResponse)
def create_attempt(
    user_id: int,
    attempt: TestAttemptCreate,
    db: Session = Depends(get_db),
):
    created_attempt = create_test_attempt(
        db,
        user_id,
        attempt,
    )

    if not created_attempt:
        raise HTTPException(
            status_code=404,
            detail="User or Test not found",
        )

    return created_attempt


@router.put("/{attempt_id}", response_model=TestAttemptResponse)
def update_attempt(
    attempt_id: int,
    attempt: TestAttemptUpdate,
    db: Session = Depends(get_db),
):
    updated_attempt = update_test_attempt(
        db,
        attempt_id,
        attempt,
    )

    if not updated_attempt:
        raise HTTPException(
            status_code=404,
            detail="Test attempt not found",
        )

    return updated_attempt


@router.delete("/{attempt_id}")
def delete_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
):
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