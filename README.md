# LMS API — FastAPI + SQLite + SQLAlchemy

A small Learning Management System REST API built for a university lab.
It runs fully locally so a teammate can clone it and test the endpoints with Postman.

## Requirements

- Python **3.10.12** (or any 3.10+)
- `pip`

## Setup & run

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --reload
```

The server is now available at **http://127.0.0.1:8000**.

- Interactive API docs (Swagger UI): **http://127.0.0.1:8000/docs**
- OpenAPI schema: **http://127.0.0.1:8000/openapi.json**

> The file `db.sqlite3` is **committed** in this repo and is already seeded with
> sample data, so no manual database setup is needed. On first launch the app
> creates tables (if missing) and seeds data only when the database is empty.

## Endpoints (8 total)

| # | Method | Path | Params | Body |
|---|--------|------|--------|------|
| 1 | GET | `/courses` | query: `search`, `category_id`, `teacher_id` | — |
| 2 | POST | `/courses` | — | `title`, `description`, `teacher_id`, `category_id` |
| 3 | PUT | `/courses/{course_id}` | path | any of: `title`, `description`, `teacher_id`, `category_id` |
| 4 | DELETE | `/courses/{course_id}` | path | — (cascades to lessons/enrollments/assignments/submissions) |
| 5 | GET | `/lessons` | query: `course_id` | — |
| 6 | POST | `/enrollments` | — | `user_id`, `course_id` |
| 7 | POST | `/submissions` | — | `assignment_id`, `user_id`, `content` |
| 8 | PUT | `/submissions/{submission_id}` | path | `score?`, `status?` |

## Seeded sample data

These IDs are available out of the box for testing:

- **Categories**: `1` Programming, `2` Mathematics, `3` Design
- **Users**: `1` Alice Teacher (teacher), `2` Bob Student (student),
  `3` Carol Student (student), `4` Admin User (admin)
- **Courses**: `1` Python Basics, `2` Linear Algebra
- **Lessons**: `1` & `2` for course 1, `3` for course 2
- **Assignments**: `1` (course 1)
- **Enrollments**: Bob (`2`) → course `1`
- **Submissions**: `1` (assignment `1`, by Bob, status `pending`)

### Example requests (Postman / curl)

```bash
# List courses, filter by search term
curl "http://127.0.0.1:8000/courses?search=Python"

# Create a course (teacher 1, category 1)
curl -X POST "http://127.0.0.1:8000/courses" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Course","description":"desc","teacher_id":1,"category_id":1}'

# Update a course
curl -X PUT "http://127.0.0.1:8000/courses/1" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title"}'

# Delete a course (cascades)
curl -X DELETE "http://127.0.0.1:8000/courses/2"

# List lessons of a course
curl "http://127.0.0.1:8000/lessons?course_id=1"

# Enroll a student
curl -X POST "http://127.0.0.1:8000/enrollments" \
  -H "Content-Type: application/json" \
  -d '{"user_id":3,"course_id":2}'

# Submit an assignment
curl -X POST "http://127.0.0.1:8000/submissions" \
  -H "Content-Type: application/json" \
  -d '{"assignment_id":1,"user_id":3,"content":"my answer"}'

# Grade a submission
curl -X PUT "http://127.0.0.1:8000/submissions/1" \
  -H "Content-Type: application/json" \
  -d '{"score":90,"status":"graded"}'
```

## Running the tests

Functional tests use `pytest` with a throwaway `test.db` (separate from the
committed `db.sqlite3`).

```bash
pip install -r requirements.txt   # already done above
pytest                            # runs tests/ against a fresh test database
```

## Project structure

```
app/
  database.py   # engine, Base, SessionLocal, get_db, PRAGMA foreign_keys=ON, init_db()
  models.py     # 7 ORM tables with cascade relationships
  schemas.py    # Pydantic v2 request/response models
  seed.py       # inserts reference + sample data
  routes.py     # the 8 endpoints
  main.py       # FastAPI app + lifespan (create tables + seed on startup)
tests/          # pytest functional tests
db.sqlite3      # committed, seeded database
requirements.txt
README.md
```
