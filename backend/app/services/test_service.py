from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.models.test import Test
from app.schemas.test import TestCreate, TestUpdate


def get_tests(db: Session):
    return db.query(Test).all()


def get_test(db: Session, test_id: int):
    return db.query(Test).filter(Test.id == test_id).first()


def create_test(db: Session, test: TestCreate):
    exam = db.query(Exam).filter(Exam.id == test.exam_id).first()

    if not exam:
        return None

    db_test = Test(**test.model_dump())

    db.add(db_test)
    db.commit()
    db.refresh(db_test)

    return db_test


def update_test(db: Session, test_id: int, test: TestUpdate):
    db_test = db.query(Test).filter(Test.id == test_id).first()

    if not db_test:
        return None

    update_data = test.model_dump(exclude_unset=True)

    if "exam_id" in update_data:
        exam = db.query(Exam).filter(
            Exam.id == update_data["exam_id"]
        ).first()

        if not exam:
            return None

    for key, value in update_data.items():
        setattr(db_test, key, value)

    db.commit()
    db.refresh(db_test)

    return db_test


def delete_test(db: Session, test_id: int):
    db_test = db.query(Test).filter(Test.id == test_id).first()

    if not db_test:
        return False

    db.delete(db_test)
    db.commit()

    return True