from sqlalchemy.orm import Session

from app.models.question import Question


class QuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, question: Question):
        self.db.add(question)
        self.db.flush()
        self.db.refresh(question)
        return question

    def get_by_id(self, question_id: int):
        return (
            self.db.query(Question)
            .filter(Question.id == question_id)
            .first()
        )

    def get_all(self):
        return self.db.query(Question).all()

    def delete(self, question: Question):
        self.db.delete(question)