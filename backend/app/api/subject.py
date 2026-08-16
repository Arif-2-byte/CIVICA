from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.subject import (
    SubjectCreate,
    SubjectResponse,
)
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


# ==========================================================
# CREATE SUBJECT
# Admin only
# ==========================================================

@router.post(
    "/",
    response_model=SubjectResponse,
)
def create(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return create_subject(
        db,
        subject,
    )


# ==========================================================
# GET ALL SUBJECTS
# Authenticated users
# ==========================================================

@router.get(
    "/",
    response_model=list[SubjectResponse],
)
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_subjects(db)


# ==========================================================
# GET ONE SUBJECT
# Authenticated users
# ==========================================================

@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def read_one(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subject = get_subject(
        db,
        subject_id,
    )

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    return subject


# ==========================================================
# UPDATE SUBJECT
# Admin only
# ==========================================================

@router.put(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def update(
    subject_id: int,
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
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


# ==========================================================
# DELETE SUBJECT
# Admin only
# ==========================================================

@router.delete("/{subject_id}")
def delete(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = delete_subject(
        db,
        subject_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    if deleted == "HAS_TOPICS":
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete this subject because "
                "it contains topics."
            ),
        )

    return {
        "message": "Subject deleted successfully"
    }