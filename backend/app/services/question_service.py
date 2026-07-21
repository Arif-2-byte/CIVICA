from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.models.exam import Exam
from app.models.question import Question
from app.models.subject import Subject
from app.models.topic import Topic
from app.schemas.pagination import PaginatedResponse
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.schemas.question_filter import QuestionFilter


def create_question(
    db: Session,
    question: QuestionCreate,
):
    db_question = Question(**question.model_dump())

    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question


def get_question(
    db: Session,
    question_id: int,
):
    return (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )


def get_questions(
    db: Session,
    filters: QuestionFilter,
):
    query = (
        db.query(Question)
        .join(Topic)
        .join(Subject)
        .join(Exam)
    )

    # -----------------------------
    # Search
    # -----------------------------
    if filters.search:
        search = f"%{filters.search}%"

        query = query.filter(
            or_(
                Question.question_text.ilike(search),
                Question.explanation.ilike(search),
            )
        )

    # -----------------------------
    # Filters
    # -----------------------------
    if filters.exam_id is not None:
        query = query.filter(
            Exam.id == filters.exam_id
        )

    if filters.subject_id is not None:
        query = query.filter(
            Subject.id == filters.subject_id
        )

    if filters.topic_id is not None:
        query = query.filter(
            Topic.id == filters.topic_id
        )

    if filters.difficulty:
        query = query.filter(
            Question.difficulty == filters.difficulty
        )

    if filters.language:
        query = query.filter(
            Question.language == filters.language
        )

    if filters.question_type:
        query = query.filter(
            Question.question_type == filters.question_type
        )

    if filters.is_pyq is not None:
        query = query.filter(
            Question.is_pyq == filters.is_pyq
        )

    if filters.year is not None:
        query = query.filter(
            Question.year == filters.year
        )

    # -----------------------------
    # Total
    # -----------------------------
    total = query.count()

    # -----------------------------
    # Sorting
    # -----------------------------
    sortable_columns = {
        "id": Question.id,
        "year": Question.year,
        "difficulty": Question.difficulty,
        "language": Question.language,
        "question_type": Question.question_type,
        "marks": Question.marks,
    }

    sort_column = sortable_columns.get(
        filters.sort_by,
        Question.id,
    )

    if filters.sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    # -----------------------------
    # Pagination
    # -----------------------------
    items = (
        query.offset(
            (filters.page - 1)
            * filters.page_size
        )
        .limit(filters.page_size)
        .all()
    )

    return PaginatedResponse.create(
        items=items,
        total=total,
        page=filters.page,
        page_size=filters.page_size,
    )


def update_question(
    db: Session,
    question_id: int,
    question: QuestionUpdate,
):
    db_question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if db_question is None:
        return None

    update_data = question.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)

    return db_question


def delete_question(
    db: Session,
    question_id: int,
):
    db_question = (
        db.query(Question)
        .filter(Question.id == question_id)
        .first()
    )

    if db_question is None:
        return None

    db.delete(db_question)
    db.commit()

    return db_question


def topic_exists(
    db: Session,
    topic_id: int,
):
    return (
        db.query(Topic)
        .filter(Topic.id == topic_id)
        .first()
        is not None
    )