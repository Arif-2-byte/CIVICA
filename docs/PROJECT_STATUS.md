# CIVICA Project Status

Last updated: 2026-07-13

## Product

CIVICA is an AI-powered learning platform for Indian competitive-exam aspirants. The initial release focuses on the study hierarchy and practice workflow: exam → subject → topic → question.

## Implemented backend capabilities

- FastAPI backend with PostgreSQL and SQLAlchemy.
- Alembic-managed database migrations.
- Registration, password hashing, JWT login, OAuth2 Swagger authorization, and `GET /users/me`.
- Exam endpoints, including seed and list operations.
- Full Subject CRUD endpoints.
- Full Topic CRUD endpoints.
- Question database model, migration, schemas, service layer, and CRUD router.

## Current database schema

| Table | Purpose |
| --- | --- |
| `users` | Accounts, credentials, selected exams, and subscription flags. |
| `exams` | Supported competitive examinations. |
| `subjects` | Subjects belonging to an exam. |
| `topics` | Topics belonging to a subject. |
| `questions` | Multiple-choice questions belonging to a topic. |
| `alembic_version` | Current database migration revision. |

## Current API surface

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/test`
- `GET /users/me` (authenticated)
- `POST /exams/seed`
- `GET /exams/`
- `POST|GET|PUT|DELETE /subjects/…`
- `POST|GET|PUT|DELETE /topics/…`
- `POST|GET|PUT|DELETE /questions/…`

## Required local verification

1. Start the backend from `backend/` with `uvicorn app.main:app --reload`.
2. Open `http://127.0.0.1:8000/docs`.
3. Confirm the five `/questions` endpoints appear.
4. Create a question using an existing `topic_id`; invalid topic IDs should return `404`.
5. Verify `correct_option` only accepts `A`, `B`, `C`, or `D`.

## Git and security status

- Do not commit `backend/.env` or Python `__pycache__` files.
- A root `.gitignore` and `backend/.env.example` are present to enforce this.
- The public repository previously tracked `backend/.env`; rotate the PostgreSQL password and JWT secret, then remove the file from Git tracking and consider purging it from history before a public release.

## Next priorities

1. Commit the Topic and Question modules after local Swagger verification.
2. Add role-based authorization so only admins can create, update, or delete academic content.
3. Build question practice attempts, scoring, and review.
4. Build the student-facing Next.js dashboard and question-practice flow.
5. Add PDF ingestion and AI study features after the core practice workflow works end to end.
