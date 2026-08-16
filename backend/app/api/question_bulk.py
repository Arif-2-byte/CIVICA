from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.question_bulk import (
    BulkOperationResponse,
    BulkQuestionRequest,
)
from app.services.question_bulk_service import (
    bulk_activate_questions,
    bulk_deactivate_questions,
    bulk_delete_questions,
)


router = APIRouter(
    prefix="/questions/bulk",
    tags=["Question Bulk Operations"],
)


# ==========================================================
# BULK DELETE
# Admin only
# ==========================================================

@router.post(
    "/delete",
    response_model=BulkOperationResponse,
    status_code=status.HTTP_200_OK,
)
def delete_questions(
    request: BulkQuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    deleted = bulk_delete_questions(
        db,
        request.question_ids,
    )

    return BulkOperationResponse(
        message=f"{deleted} question(s) deleted successfully.",
        affected_rows=deleted,
    )


# ==========================================================
# BULK ACTIVATE
# Admin only
# ==========================================================

@router.patch(
    "/activate",
    response_model=BulkOperationResponse,
)
def activate_questions(
    request: BulkQuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    updated = bulk_activate_questions(
        db,
        request.question_ids,
    )

    return BulkOperationResponse(
        message=f"{updated} question(s) activated successfully.",
        affected_rows=updated,
    )


# ==========================================================
# BULK DEACTIVATE
# Admin only
# ==========================================================

@router.patch(
    "/deactivate",
    response_model=BulkOperationResponse,
)
def deactivate_questions(
    request: BulkQuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    updated = bulk_deactivate_questions(
        db,
        request.question_ids,
    )

    return BulkOperationResponse(
        message=f"{updated} question(s) deactivated successfully.",
        affected_rows=updated,
    )