import app.models
from app.db.session import SessionLocal

from app.seeds.users import seed_users
from app.seeds.exams import seed_exams
from app.seeds.subjects import seed_subjects
from app.seeds.topics import seed_topics
from app.seeds.questions import seed_questions


def run_seed():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("🌱 CIVICA DATABASE SEEDER")
        print("=" * 60)

        seed_users(db)
        seed_exams(db)
        seed_subjects(db)
        seed_topics(db)
        seed_questions(db)

        print("\n🎉 Database seeding completed successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()