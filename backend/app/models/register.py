# Import every SQLAlchemy model once so relationship() can resolve them.

from app.models.user import User
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.question import Question
from app.models.test import Test
from app.models.test_attempt import TestAttempt
from app.models.attempt_question import AttemptQuestion
from app.models.test_question import TestQuestion