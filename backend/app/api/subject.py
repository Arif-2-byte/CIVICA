from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.subject import SubjectCreate, SubjectResponse
from app.services.subject_service import (
    create_subject,
    delete_subject,
    get_subject,
    get_subjects,
    update_subject,
)

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
)


@router.post("/", response_model=SubjectResponse)
def create(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
):
    return create_subject(db, subject)


@router.get("/", response_model=list[SubjectResponse])
def read_all(
    db: Session = Depends(get_db),
):
    return get_subjects(db)


@router.get("/{subject_id}", response_model=SubjectResponse)
def read_one(
    subject_id: int,
    db: Session = Depends(get_db),
):
    subject = get_subject(db, subject_id)

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update(
    subject_id: int,
    subject: SubjectCreate,
    db: Session = Depends(get_db),
):
    updated = update_subject(
        db,
        subject_id,
        subject,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    return updated


@router.delete("/{subject_id}")
def delete(
    subject_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_subject(
        db,
        subject_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    return {
        "message": "Subject deleted successfully"
    }