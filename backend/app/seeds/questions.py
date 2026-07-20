import csv
import os

from app.models.question import Question
from app.models.subject import Subject
from app.models.topic import Topic


def seed_questions(db):
    """Import questions from CSV files."""

    data_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "data",
    )

    csv_files = [
        "upsc_history.csv",
    ]

    total_imported = 0
    total_duplicates = 0
    total_errors = 0

    for file_name in csv_files:

        file_path = os.path.join(data_folder, file_name)

        if not os.path.exists(file_path):
            print(f"⚠ File not found: {file_name}")
            continue

        print(f"\n📄 Importing {file_name}")

        with open(file_path, newline="", encoding="utf-8") as csvfile:

            reader = csv.DictReader(csvfile)

            for row_number, row in enumerate(reader, start=2):

                try:

                    subject = (
                        db.query(Subject)
                        .filter(Subject.name == row["subject"])
                        .first()
                    )

                    if not subject:
                        print(
                            f"❌ Row {row_number}: Subject '{row['subject']}' not found."
                        )
                        total_errors += 1
                        continue

                    topic = (
                        db.query(Topic)
                        .filter(
                            Topic.name == row["topic"],
                            Topic.subject_id == subject.id,
                        )
                        .first()
                    )

                    if not topic:
                        print(
                            f"❌ Row {row_number}: Topic '{row['topic']}' not found."
                        )
                        total_errors += 1
                        continue

                    duplicate = (
                        db.query(Question)
                        .filter(
                            Question.question_text == row["question"],
                        )
                        .first()
                    )

                    if duplicate:
                        total_duplicates += 1
                        continue

                    question = Question(
                        question_text=row["question"],
                        option_a=row["option_a"],
                        option_b=row["option_b"],
                        option_c=row["option_c"],
                        option_d=row["option_d"],
                        correct_option=row["correct_option"],
                        explanation=row["explanation"],
                        difficulty=row["difficulty"],
                        marks=int(row["marks"]),
                        negative_marks=float(row["negative_marks"]),
                        year=int(row["year"]) if row["year"] else None,
                        source=row["source"],
                        language=row["language"],
                        question_type=row["question_type"],
                        exam_stage=row["exam_stage"],
                        is_pyq=row["is_pyq"].lower() == "true",
                        tags=row["tags"],
                        estimated_time=int(row["estimated_time"]),
                        hint=row["hint"],
                        topic_id=topic.id,
                    )

                    db.add(question)

                    total_imported += 1

                except Exception as e:
                    total_errors += 1
                    print(f"❌ Row {row_number}: {e}")

    db.commit()

    print("\n==============================")
    print("QUESTION IMPORT SUMMARY")
    print("==============================")
    print(f"✅ Imported : {total_imported}")
    print(f"⚠ Duplicates: {total_duplicates}")
    print(f"❌ Errors    : {total_errors}")
    print("==============================")