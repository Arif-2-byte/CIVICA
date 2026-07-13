from fastapi import FastAPI

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

app = FastAPI(
    title="CIVICA API"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(exam_router)
app.include_router(subject_router)
app.include_router(topic_router)
app.include_router(question_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CIVICA API"
    }
