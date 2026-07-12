from fastapi import FastAPI

from app.auth.auth import router as auth_router
from app.db.database import Base, engine
from app.models.user import User
from app.users.user import router as user_router
from app.models.exam import Exam
from app.api.exam import router as exam_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CIVICA API"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(exam_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CIVICA API"
    }