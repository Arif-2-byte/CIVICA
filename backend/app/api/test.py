from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.test import TestCreate, TestResponse, TestUpdate
from app.services.test_service import (
    create_test,
    delete_test,
    get_test,
    get_tests,
    update_test,
)

router = APIRouter(
    prefix="/tests",
    tags=["Tests"],
)


@router.get("/", response_model=list[TestResponse])
def read_tests(db: Session = Depends(get_db)):
    return get_tests(db)


@router.get("/{test_id}", response_model=TestResponse)
def read_test(test_id: int, db: Session = Depends(get_db)):
    test = get_test(db, test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    return test


@router.post("/", response_model=TestResponse)
def create_new_test(
    test: TestCreate,
    db: Session = Depends(get_db),
):
    new_test = create_test(db, test)

    if not new_test:
        raise HTTPException(
            status_code=404,
            detail="Exam not found",
        )

    return new_test


@router.put("/{test_id}", response_model=TestResponse)
def update_existing_test(
    test_id: int,
    test: TestUpdate,
    db: Session = Depends(get_db),
):
    updated_test = update_test(
        db,
        test_id,
        test,
    )

    if not updated_test:
        raise HTTPException(
            status_code=404,
            detail="Test or Exam not found",
        )

    return updated_test


@router.delete("/{test_id}")
def remove_test(
    test_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_test(db, test_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Test not found",
        )

    return {"message": "Test deleted successfully"}