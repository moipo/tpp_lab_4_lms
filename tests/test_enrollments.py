def test_create_enrollment(client):
    # Carol (user 3) enrolls in course 2.
    r = client.post("/enrollments", json={"user_id": 3, "course_id": 2})
    assert r.status_code == 201
    body = r.json()
    assert body["user_id"] == 3
    assert body["course_id"] == 2


def test_create_enrollment_duplicate(client):
    # Bob (user 2) is already enrolled in course 1 via seed data.
    r = client.post("/enrollments", json={"user_id": 2, "course_id": 1})
    assert r.status_code == 409


def test_create_enrollment_missing_user(client):
    r = client.post("/enrollments", json={"user_id": 9999, "course_id": 1})
    assert r.status_code == 404


def test_create_enrollment_missing_course(client):
    r = client.post("/enrollments", json={"user_id": 2, "course_id": 9999})
    assert r.status_code == 404
