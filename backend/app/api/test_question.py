from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.user import User
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


# ==========================================================
# CREATE TEST QUESTION
# Admin only
# ==========================================================

@router.post(
    "/",
    response_model=TestQuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    test_question: TestQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    result = create_test_question(
        db,
        test_question,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Test or Question not found",
        )

    return result


# ==========================================================
# GET ALL TEST QUESTIONS
# Authenticated users
# ==========================================================

@router.get(
    "/",
    response_model=list[TestQuestionResponse],
)
def read_all(
    test_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_test_questions(
        db,
        test_id,
    )


# ==========================================================
# GET ONE TEST QUESTION
# Authenticated users
# ==========================================================

@router.get(
    "/{test_question_id}",
    response_model=TestQuestionResponse,
)
def read_one(
    test_question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = get_test_question(
        db,
        test_question_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Test question not found",
        )

    return result


# ==========================================================
# UPDATE TEST QUESTION
# Admin only
# ==========================================================

@router.put(
    "/{test_question_id}",
    response_model=TestQuestionResponse,
)
def update(
    test_question_id: int,
    test_question: TestQuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    result = update_test_question(
        db,
        test_question_id,
        test_question,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Test question not found",
        )

    return result


# ==========================================================
# DELETE TEST QUESTION
# Admin only
# ==========================================================

@router.delete(
    "/{test_question_id}",
)
def delete(
    test_question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = delete_test_question(
        db,
        test_question_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Test question not found",
        )

    if deleted == "USED_IN_ATTEMPT":
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete this test question because "
                "it is already used in a student attempt."
            ),
        )

    return {
        "message": "Test question deleted successfully"
    }