from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.services.question_service import (
    create_question,
    delete_question,
    get_question,
    get_questions,
    topic_exists,
    update_question,
)

router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create(
    question: QuestionCreate,
    db: Session = Depends(get_db),
):
    if not topic_exists(db, question.topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")
    return create_question(db, question)


@router.get("/", response_model=list[QuestionResponse])
def read_all(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_questions(db, skip=skip, limit=limit)


@router.get("/{question_id}", response_model=QuestionResponse)
def read_one(
    question_id: int,
    db: Session = Depends(get_db),
):
    question = get_question(db, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
def update(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db),
):
    if question.topic_id is not None and not topic_exists(db, question.topic_id):
        raise HTTPException(status_code=404, detail="Topic not found")

    updated_question = update_question(db, question_id, question)
    if updated_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return updated_question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    question_id: int,
    db: Session = Depends(get_db),
):
    deleted_question = delete_question(db, question_id)
    if deleted_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
