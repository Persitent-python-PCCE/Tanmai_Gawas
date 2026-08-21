# tests/test_course_module_lesson.py
"""Integration tests for Phase 2 – Course, Module & Lesson management.
These tests use the Flask test client and assume the app factory is
`create_app` from `app.py`. Authentication is performed via the `/login`
endpoint; the returned session cookie is reused for subsequent requests.
Only high‑level happy‑path and a few negative‑case checks are included –
more exhaustive edge‑case tests can be added later.
"""

import json
import pytest
from app import create_app
from config.db import db as _db
from models.user import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope="module")
def app():
    """Create a Flask app instance bound to a temporary SQLite DB.
    The real project uses MySQL, but for unit tests an in‑memory SQLite
    database is sufficient and fast.
    """
    test_config = type("Config", (), {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "WTF_CSRF_ENABLED": False,
    })
    app = create_app(test_config)
    with app.app_context():
        _db.create_all()
        # create a default instructor user for auth‑protected endpoints
        instructor = User(
            email="instructor@example.com",
            password_hash=generate_password_hash("StrongPass1"),
            role="instructor",
        )
        _db.session.add(instructor)
        _db.session.commit()
    yield app
    # teardown – drop all tables
    with app.app_context():
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def login_as_instructor(client):
    resp = client.post(
        "/login",
        data=json.dumps({"email": "instructor@example.com", "password": "StrongPass1"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    # Flask‑Login stores the session cookie automatically; the client retains it.
    return client

def test_course_crud(login_as_instructor):
    client = login_as_instructor
    # --- CREATE ---------------------------------------------------
    create_resp = client.post(
        "/courses",
        data=json.dumps({"title": "Python 101", "description": "Intro to Python"}),
        content_type="application/json",
    )
    assert create_resp.status_code == 201
    course_id = json.loads(create_resp.data)["id"]

    # --- READ (list) --------------------------------------------
    list_resp = client.get("/courses")
    assert list_resp.status_code == 200
    courses = json.loads(list_resp.data)
    assert any(c["id"] == course_id for c in courses)

    # --- READ (single) ------------------------------------------
    get_resp = client.get(f"/courses/{course_id}")
    assert get_resp.status_code == 200
    data = json.loads(get_resp.data)
    assert data["title"] == "Python 101"

    # --- UPDATE ------------------------------------------------
    upd_resp = client.put(
        f"/courses/{course_id}",
        data=json.dumps({"title": "Python Basics"}),
        content_type="application/json",
    )
    assert upd_resp.status_code == 200
    # verify change
    get_resp = client.get(f"/courses/{course_id}")
    assert json.loads(get_resp.data)["title"] == "Python Basics"

    # --- DELETE ------------------------------------------------
    del_resp = client.delete(f"/courses/{course_id}")
    assert del_resp.status_code == 200
    # confirm gone
    get_resp = client.get(f"/courses/{course_id}")
    assert get_resp.status_code == 404

def test_module_and_lesson_flow(login_as_instructor):
    client = login_as_instructor
    # create a course to own modules/lessons
    cr = client.post(
        "/courses",
        data=json.dumps({"title": "Web Dev", "description": "Full‑stack"}),
        content_type="application/json",
    )
    course_id = json.loads(cr.data)["id"]

    # --- MODULE CREATE ------------------------------------------
    mod_resp = client.post(
        f"/courses/{course_id}/modules",
        data=json.dumps({"title": "HTML Basics", "description": "Tags & semantics"}),
        content_type="application/json",
    )
    assert mod_resp.status_code == 201
    module_id = json.loads(mod_resp.data)["id"]

    # --- LESSON CREATE ------------------------------------------
    lesson_payload = {
        "title": "Heading Tags",
        "content": "# H1\n## H2\n### H3",
    }
    les_resp = client.post(
        f"/modules/{module_id}/lessons",
        data=json.dumps(lesson_payload),
        content_type="application/json",
    )
    assert les_resp.status_code == 201
    lesson_id = json.loads(les_resp.data)["id"]

    # --- LESSON READ -------------------------------------------
    get_lesson = client.get(
        f"/modules/{module_id}/lessons/{lesson_id}"
    )
    assert get_lesson.status_code == 200
    lesson_data = json.loads(get_lesson.data)
    assert lesson_data["title"] == "Heading Tags"
    assert "# H1" in lesson_data["content"]

    # --- CLEANUP ------------------------------------------------
    client.delete(f"/modules/{module_id}/lessons/{lesson_id}")
    client.delete(f"/courses/{course_id}/modules/{module_id}")
    client.delete(f"/courses/{course_id}")
