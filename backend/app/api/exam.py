from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.jwt_handler import (
    get_current_user,
    require_admin,
)
from app.db.session import get_db
from app.models.exam import Exam
from app.models.user import User
from app.schemas.exam import ExamResponse
from app.services.exam_service import seed_exams


router = APIRouter(
    prefix="/exams",
    tags=["Exams"],
)


# ==========================================================
# SEED EXAMS
# Admin only
# ==========================================================

@router.post("/seed")
def seed(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    seed_exams(db)

    return {
        "message": "Exams seeded successfully."
    }


# ==========================================================
# GET EXAMS
# Authenticated users
# ==========================================================

@router.get(
    "/",
    response_model=list[ExamResponse],
)
def get_exams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Exam)
        .filter(
            Exam.is_active == True
        )
        .order_by(Exam.name)
        .all()
    )