from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.attempt_question import AttemptQuestion
from app.models.user import User
from app.schemas.attempt_question import (
    AttemptQuestionCreate,
    AttemptQuestionResponse,
)
from app.services.attempt_question_service import (
    create_attempt_question,
    delete_attempt_question,
    get_attempt_question,
    get_attempt_questions,
)


router = APIRouter(
    prefix="/attempt-questions",
    tags=["Attempt Questions"],
)


# ==========================================================
# GET ALL ATTEMPT QUESTIONS
# Admin only
# ==========================================================

@router.get(
    "/",
    response_model=list[AttemptQuestionResponse],
)
def read_attempt_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return get_attempt_questions(db)


# ==========================================================
# GET ONE ATTEMPT QUESTION
# Owner or Admin
# ==========================================================

@router.get(
    "/{attempt_question_id}",
    response_model=AttemptQuestionResponse,
)
def read_attempt_question(
    attempt_question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    attempt_question = get_attempt_question(
        db,
        attempt_question_id,
    )

    if not attempt_question:
        raise HTTPException(
            status_code=404,
            detail="Attempt question not found",
        )

    # Admin can access any attempt question.
    if current_user.role == "admin":
        return attempt_question

    # Get the associated attempt.
    attempt = attempt_question.attempt

    if attempt is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt question not found",
        )

    # Student can access only their own attempt.
    if attempt.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this attempt question",
        )

    return attempt_question


# ==========================================================
# CREATE ATTEMPT QUESTION
# Admin only
# Normally created automatically by test-attempt service
# ==========================================================

@router.post(
    "/",
    response_model=AttemptQuestionResponse,
)
def create_new_attempt_question(
    attempt_question: AttemptQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return create_attempt_question(
        db,
        attempt_question,
    )


# ==========================================================
# DELETE ATTEMPT QUESTION
# Admin only
# ==========================================================

@router.delete(
    "/{attempt_question_id}",
)
def remove_attempt_question(
    attempt_question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = delete_attempt_question(
        db,
        attempt_question_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Attempt question not found",
        )

    return {
        "message": "Attempt question deleted successfully"
    }