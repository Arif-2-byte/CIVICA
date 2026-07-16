import app.models.register

from app.db.session import SessionLocal

from app.seeders.exams import seed_exams
from app.seeders.subjects import seed_subjects
from app.seeders.topics import seed_topics


def run():
    db = SessionLocal()

    try:
        print("=" * 50)
        print("CIVICA Exam Database Seeder")
        print("=" * 50)

        print("\nSeeding Exams...")
        seed_exams(db)

        print("✓ Exams completed")

        print("\nSeeding Subjects...")
        seed_subjects(db)

        print("✓ Subjects completed")

        print("\nSeeding Topics...")
        seed_topics(db)

        print("✓ Topics completed")

        print("\n" + "=" * 50)
        print("Exam database seeded successfully!")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f"\nError: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    run()