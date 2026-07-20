from pydantic import BaseModel


class AdminDashboard(BaseModel):
    total_users: int

    total_exams: int

    total_subjects: int

    total_topics: int

    total_questions: int

    total_tests: int

    total_attempts: int

    completed_attempts: int

    average_score: float

    class Config:
        from_attributes = True