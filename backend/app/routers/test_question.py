from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.test_question import (
    TestQuestionCreate,
    TestQuestionResponse,
    TestQuestionUpdate,
)
from app.services.test_question_service import (
    create_test_question,
    delete_test_question,
    get_test_question,
    get_test_questions,
    update_test_question,
)

router = APIRouter(
    prefix="/test-questions",
    tags=["Test Questions"],
)


@router.get("/", response_model=list[TestQuestionResponse])
def read_test_questions(
    db: Session = Depends(get_db),
):
    return get_test_questions(db)


@router.get("/{test_question_id}", response_model=TestQuestionResponse)
def read_test_question(
    test_question_id: int,
    db: Session = Depends(get_db),
):
    test_question = get_test_question(
        db,
        test_question_id,
    )

    if not test_question:
        raise HTTPException(
            status_code=404,
            detail="Test Question not found",
        )

    return test_question


@router.post("/", response_model=TestQuestionResponse)
def create_new_test_question(
    test_question: TestQuestionCreate,
    db: Session = Depends(get_db),
):
    new_test_question = create_test_question(
        db,
        test_question,
    )

    if not new_test_question:
        raise HTTPException(
            status_code=404,
            detail="Test or Question not found",
        )

    return new_test_question


@router.put("/{test_question_id}", response_model=TestQuestionResponse)
def update_existing_test_question(
    test_question_id: int,
    test_question: TestQuestionUpdate,
    db: Session = Depends(get_db),
):
    updated_test_question = update_test_question(
        db,
        test_question_id,
        test_question,
    )

    if not updated_test_question:
        raise HTTPException(
            status_code=404,
            detail="Test Question not found",
        )

    return updated_test_question


@router.delete("/{test_question_id}")
def remove_test_question(
    test_question_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_test_question(
        db,
        test_question_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Test Question not found",
        )

    return {
        "message": "Test Question deleted successfully"
    }