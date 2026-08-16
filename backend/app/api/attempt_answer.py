from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import get_current_user
from app.db.session import get_db
from app.models.attempt_answer import AttemptAnswer
from app.models.test_attempt import TestAttempt
from app.models.user import User
from app.schemas.attempt_answer import (
    AttemptAnswerCreate,
    AttemptAnswerResponse,
    AttemptAnswerUpdate,
)
from app.services import attempt_answer_service


router = APIRouter(
    prefix="/attempt-answers",
    tags=["Attempt Answers"],
)


def verify_attempt_access(
    db: Session,
    attempt_id: int,
    current_user: User,
):
    attempt = (
        db.query(TestAttempt)
        .filter(
            TestAttempt.id == attempt_id
        )
        .first()
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


@router.get(
    "/",
    response_model=list[AttemptAnswerResponse],
)
def get_attempt_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        return attempt_answer_service.get_attempt_answers(db)

    raise HTTPException(
        status_code=403,
        detail="Admin access required.",
    )


@router.get(
    "/{answer_id}",
    response_model=AttemptAnswerResponse,
)
def get_attempt_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    answer = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.id == answer_id
        )
        .first()
    )

    if answer is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    verify_attempt_access(
        db,
        answer.attempt_id,
        current_user,
    )

    return answer


@router.post(
    "/",
    response_model=AttemptAnswerResponse,
)
def create_attempt_answer(
    answer: AttemptAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    verify_attempt_access(
        db,
        answer.attempt_id,
        current_user,
    )

    return attempt_answer_service.create_attempt_answer(
        db,
        answer,
    )


@router.put(
    "/{answer_id}",
    response_model=AttemptAnswerResponse,
)
def update_attempt_answer(
    answer_id: int,
    answer: AttemptAnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_answer = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.id == answer_id
        )
        .first()
    )

    if existing_answer is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    verify_attempt_access(
        db,
        existing_answer.attempt_id,
        current_user,
    )

    return attempt_answer_service.update_attempt_answer(
        db,
        answer_id,
        answer,
    )


@router.delete(
    "/{answer_id}",
)
def delete_attempt_answer(
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_answer = (
        db.query(AttemptAnswer)
        .filter(
            AttemptAnswer.id == answer_id
        )
        .first()
    )

    if existing_answer is None:
        raise HTTPException(
            status_code=404,
            detail="Attempt Answer not found",
        )

    verify_attempt_access(
        db,
        existing_answer.attempt_id,
        current_user,
    )

    return attempt_answer_service.delete_attempt_answer(
        db,
        answer_id,
    )