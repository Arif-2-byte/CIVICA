from app.core.security import get_password_hash
from app.models.user import User


def seed_users(db):
    """Seed default users."""

    if db.query(User).count() > 0:
        print("✔ Users already seeded")
        return

    users = [
        User(
            username="admin",
            email="admin@civica.com",
            hashed_password=get_password_hash("Admin@123"),
            full_name="System Administrator",
            exams="UPSC,JKPSC,SSC",
            is_active=True,
            is_verified=True,
            is_premium=True,
        ),
        User(
            username="student1",
            email="student1@civica.com",
            hashed_password=get_password_hash("Student@123"),
            full_name="Demo Student One",
            exams="UPSC",
            is_active=True,
            is_verified=True,
            is_premium=False,
        ),
        User(
            username="student2",
            email="student2@civica.com",
            hashed_password=get_password_hash("Student@123"),
            full_name="Demo Student Two",
            exams="JKPSC",
            is_active=True,
            is_verified=True,
            is_premium=False,
        ),
    ]

    db.add_all(users)
    db.commit()

    print("✔ Users seeded")