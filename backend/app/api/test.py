from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.question import QuestionResponse
from app.schemas.test import (
    TestCreate,
    TestResponse,
    TestUpdate,
)
from app.services.test_service import (
    create_test,
    delete_test,
    get_test,
    get_tests,
    get_test_questions,
    update_test,
)


router = APIRouter(
    prefix="/tests",
    tags=["Tests"],
)


# ==========================================================
# CREATE TEST
# Admin only
# ==========================================================

@router.post(
    "/",
    response_model=TestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    test: TestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_test = create_test(
        db,
        test,
    )

    if db_test is None:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    return db_test


# ==========================================================
# GET ALL TESTS
# Authenticated users
# ==========================================================

@router.get(
    "/",
    response_model=list[TestResponse],
)
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_tests(db)


# ==========================================================
# GET TEST QUESTIONS
# Authenticated users
# ==========================================================

@router.get(
    "/{test_id}/questions",
    response_model=list[QuestionResponse],
)
def read_test_questions(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    questions = get_test_questions(
        db,
        test_id,
    )

    if questions is None:
        raise HTTPException(
            status_code=404,
            detail="Test not found",
        )

    return questions


# ==========================================================
# GET ONE TEST
# Authenticated users
# ==========================================================

@router.get(
    "/{test_id}",
    response_model=TestResponse,
)
def read_one(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_test = get_test(
        db,
        test_id,
    )

    if db_test is None:
        raise HTTPException(
            status_code=404,
            detail="Test not found",
        )

    return db_test


# ==========================================================
# UPDATE TEST
# Admin only
# ==========================================================

@router.put(
    "/{test_id}",
    response_model=TestResponse,
)
def update(
    test_id: int,
    test: TestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_test = update_test(
        db,
        test_id,
        test,
    )

    if db_test is None:
        raise HTTPException(
            status_code=404,
            detail="Test or Exam not found",
        )

    return db_test


# ==========================================================
# DELETE TEST
# Admin only
# ==========================================================

@router.delete(
    "/{test_id}",
)
def delete(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_test = delete_test(
        db,
        test_id,
    )

    if db_test is None:
        raise HTTPException(
            status_code=404,
            detail="Test not found",
        )

    if db_test == "HAS_QUESTIONS":
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete this test because "
                "it has questions assigned to it."
            ),
        )

    if db_test == "HAS_ATTEMPTS":
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete this test because "
                "students have already attempted it."
            ),
        )

    return {
        "message": "Test deleted successfully"
    }