from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.exam import Exam
from app.schemas.exam import ExamResponse
from app.services.exam_service import seed_exams

router = APIRouter(
    prefix="/exams",
    tags=["Exams"],
)


@router.post("/seed")
def seed(db: Session = Depends(get_db)):
    seed_exams(db)
    return {
        "message": "Exams seeded successfully."
    }


@router.get("/", response_model=list[ExamResponse])
def get_exams(db: Session = Depends(get_db)):
    return (
        db.query(Exam)
        .filter(Exam.is_active == True)
        .order_by(Exam.name)
        .all()
    )