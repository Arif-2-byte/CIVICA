from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

from app.core.middleware import log_requests
from app.auth.auth import router as auth_router
from app.db.database import Base, engine
from app.models.user import User
from app.users.user import router as user_router
from app.models.exam import Exam
from app.api.exam import router as exam_router
from app.models.subject import Subject
from app.api.subject import router as subject_router
from app.models.topic import Topic
from app.api.topic import router as topic_router
from app.models.question import Question
from app.api.question import router as question_router
from app.models.test import Test
from app.api.test import router as test_router
from app.models.test_attempt import TestAttempt
from app.api.test_attempt import router as test_attempt_router
from app.models.attempt_question import AttemptQuestion
from app.models.attempt_answer import AttemptAnswer
from app.api import test_question
from app.api import attempt_answer
from app.api import result
from app.api import answer_review
from app.api import subject_analytics
from app.api import topic_analytics
from app.api import dashboard
from app.api import admin_dashboard
from app.models.mistake_notebook import MistakeNotebook
from app.api import mistake_notebook
from app.api.attempt_question import (
    router as attempt_question_router,
)
app = FastAPI(
    title="CIVICA API"
)

app.middleware("http")(log_requests)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(exam_router)
app.include_router(subject_router)
app.include_router(topic_router)
app.include_router(question_router)
app.include_router(test_router)
app.include_router(test_attempt_router)
app.include_router(attempt_question_router)
app.include_router(test_question.router)
app.include_router(attempt_answer.router)
app.include_router(result.router)
app.include_router(answer_review.router)
app.include_router(subject_analytics.router)
app.include_router(topic_analytics.router)
app.include_router(dashboard.router)
app.include_router(admin_dashboard.router)
app.include_router(mistake_notebook.router)
app.openapi_schema = None

@app.get("/")
def root():
    return {
        "message": "Welcome to CIVICA API"
    }