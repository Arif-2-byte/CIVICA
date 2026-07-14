from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
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


@router.get("/", response_model=list[AttemptQuestionResponse])
def read_attempt_questions(
    db: Session = Depends(get_db),
):
    return get_attempt_questions(db)


@router.get("/{attempt_question_id}", response_model=AttemptQuestionResponse)
def read_attempt_question(
    attempt_question_id: int,
    db: Session = Depends(get_db),
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

    return attempt_question


@router.post("/", response_model=AttemptQuestionResponse)
def create_new_attempt_question(
    attempt_question: AttemptQuestionCreate,
    db: Session = Depends(get_db),
):
    return create_attempt_question(
        db,
        attempt_question,
    )


@router.delete("/{attempt_question_id}")
def remove_attempt_question(
    attempt_question_id: int,
    db: Session = Depends(get_db),
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