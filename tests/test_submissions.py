def test_create_submission(client):
    r = client.post(
        "/submissions",
        json={"assignment_id": 1, "user_id": 3, "content": "my answer"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "pending"
    assert body["score"] is None
    assert body["content"] == "my answer"


def test_create_submission_missing_assignment(client):
    r = client.post(
        "/submissions",
        json={"assignment_id": 9999, "user_id": 3, "content": "x"},
    )
    assert r.status_code == 404


def test_update_submission_grade(client):
    # Submission id 1 is seeded.
    r = client.put("/submissions/1", json={"score": 90, "status": "graded"})
    assert r.status_code == 200
    body = r.json()
    assert body["score"] == 90
    assert body["status"] == "graded"


def test_update_submission_missing(client):
    r = client.put("/submissions/9999", json={"score": 10})
    assert r.status_code == 404
