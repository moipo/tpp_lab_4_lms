from app.database import SessionLocal
from app import models


def test_list_courses(client):
    r = client.get("/courses")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 2


def test_filter_courses_search(client):
    r = client.get("/courses?search=Python")
    assert r.status_code == 200
    titles = [c["title"] for c in r.json()]
    assert "Python Basics" in titles


def test_filter_courses_category(client):
    r = client.get("/courses?category_id=2")
    assert r.status_code == 200
    body = r.json()
    assert all(c["category_id"] == 2 for c in body)
    assert any(c["title"] == "Linear Algebra" for c in body)


def test_filter_courses_teacher(client):
    r = client.get("/courses?teacher_id=1")
    assert r.status_code == 200
    assert all(c["teacher_id"] == 1 for c in r.json())


def test_create_course(client):
    payload = {
        "title": "Test Course",
        "description": "A course created in a test",
        "teacher_id": 1,
        "category_id": 1,
    }
    r = client.post("/courses", json=payload)
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Test Course"
    assert body["id"] > 0


def test_create_course_missing_teacher(client):
    payload = {
        "title": "x",
        "description": "d",
        "teacher_id": 9999,
        "category_id": 1,
    }
    r = client.post("/courses", json=payload)
    assert r.status_code == 404


def test_update_course(client):
    r = client.put("/courses/1", json={"title": "Python Basics (updated)"})
    assert r.status_code == 200
    assert r.json()["title"] == "Python Basics (updated)"


def test_delete_course_cascade(client):
    # Create a course with a child lesson directly to verify cascade delete.
    db = SessionLocal()
    try:
        course = models.Course(
            title="Cascade Course",
            description="d",
            teacher_id=1,
            category_id=1,
            created_at="2026-01-01T00:00:00",
        )
        db.add(course)
        db.flush()
        db.add(models.Lesson(course_id=course.id, title="L", content="c", position=1))
        db.commit()
        cid = course.id
    finally:
        db.close()

    r = client.get(f"/lessons?course_id={cid}")
    assert r.status_code == 200 and len(r.json()) == 1

    r = client.delete(f"/courses/{cid}")
    assert r.status_code == 204

    # Child lesson removed by cascade, and course no longer listed.
    r = client.get(f"/lessons?course_id={cid}")
    assert r.status_code == 200 and r.json() == []
    ids = [c["id"] for c in client.get("/courses").json()]
    assert cid not in ids
