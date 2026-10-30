from datetime import datetime

from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app import models


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def seed_data():
    # Ensure tables exist (idempotent) so this also works when run standalone.
    init_db()
    db: Session = SessionLocal()
    try:
        # Already seeded -> do nothing (keeps the committed db intact).
        if db.query(models.User).first() is not None:
            return

        prog = models.Category(name="Programming")
        math = models.Category(name="Mathematics")
        design = models.Category(name="Design")
        db.add_all([prog, math, design])
        db.flush()

        alice = models.User(
            email="alice@lms.dev",
            full_name="Alice Teacher",
            password_hash="plain",
            role="teacher",
            created_at=now_iso(),
        )
        bob = models.User(
            email="bob@lms.dev",
            full_name="Bob Student",
            password_hash="plain",
            role="student",
            created_at=now_iso(),
        )
        carol = models.User(
            email="carol@lms.dev",
            full_name="Carol Student",
            password_hash="plain",
            role="student",
            created_at=now_iso(),
        )
        admin = models.User(
            email="admin@lms.dev",
            full_name="Admin User",
            password_hash="plain",
            role="admin",
            created_at=now_iso(),
        )
        db.add_all([alice, bob, carol, admin])
        db.flush()

        c1 = models.Course(
            title="Python Basics",
            description="Introduction to Python programming",
            teacher_id=alice.id,
            category_id=prog.id,
            created_at=now_iso(),
        )
        c2 = models.Course(
            title="Linear Algebra",
            description="Vectors, matrices and transformations",
            teacher_id=alice.id,
            category_id=math.id,
            created_at=now_iso(),
        )
        db.add_all([c1, c2])
        db.flush()

        lessons = [
            models.Lesson(
                course_id=c1.id, title="Hello World", content="Your first print()", position=1
            ),
            models.Lesson(
                course_id=c1.id, title="Variables", content="Variables and types", position=2
            ),
            models.Lesson(
                course_id=c2.id, title="Vectors", content="Vector basics", position=1
            ),
        ]
        db.add_all(lessons)

        a1 = models.Assignment(
            course_id=c1.id,
            title="First Script",
            description="Write a small Python script",
            max_score=100,
            due_at=now_iso(),
        )
        db.add(a1)
        db.flush()

        enrollment = models.Enrollment(
            user_id=bob.id, course_id=c1.id, enrolled_at=now_iso()
        )
        db.add(enrollment)

        submission = models.Submission(
            assignment_id=a1.id,
            user_id=bob.id,
            content="Here is my solution",
            score=None,
            status="pending",
            submitted_at=now_iso(),
        )
        db.add(submission)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
