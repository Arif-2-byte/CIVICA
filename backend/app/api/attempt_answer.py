from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
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


@router.get(
    "/",
    response_model=list[AttemptAnswerResponse],
)
def get_attempt_answers(db: Session = Depends(get_db)):
    return attempt_answer_service.get_attempt_answers(db)


@router.get(
    "/{answer_id}",
    response_model=AttemptAnswerResponse,
)
def get_attempt_answer(
    answer_id: int,
    db: Session = Depends(get_db),
):
    return attempt_answer_service.get_attempt_answer(
        db,
        answer_id,
    )


@router.post(
    "/",
    response_model=AttemptAnswerResponse,
)
def create_attempt_answer(
    answer: AttemptAnswerCreate,
    db: Session = Depends(get_db),
):
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
):
    return attempt_answer_service.update_attempt_answer(
        db,
        answer_id,
        answer,
    )


@router.delete("/{answer_id}")
def delete_attempt_answer(
    answer_id: int,
    db: Session = Depends(get_db),
):
    return attempt_answer_service.delete_attempt_answer(
        db,
        answer_id,
    )