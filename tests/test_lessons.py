def test_list_lessons_all(client):
    r = client.get("/lessons")
    assert r.status_code == 200
    assert len(r.json()) >= 3


def test_list_lessons_filter(client):
    r = client.get("/lessons?course_id=1")
    assert r.status_code == 200
    body = r.json()
    assert len(body) >= 2
    assert all(l["course_id"] == 1 for l in body)
