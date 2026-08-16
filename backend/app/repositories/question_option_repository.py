from sqlalchemy.orm import Session

from app.models.question_option import QuestionOption


class QuestionOptionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, option: QuestionOption):
        self.db.add(option)