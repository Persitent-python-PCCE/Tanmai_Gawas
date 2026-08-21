import pytest
from app import create_app
from flask import url_for

from config.config import TestingConfig
from config.db import db

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()
    ctx.pop()

@pytest.fixture
def client(app):
    return app.test_client()

def test_material_download_requires_enrollment(client):
    from dao.course_dao import create_course
    from dao.module_dao import create_module
    from dao.user_dao import create_user
    instructor = create_user(email='inst_mat@example.com', password_hash='hash', role='instructor')
    course = create_course(title='MatCourse2', description='', instructor_id=instructor.id)
    module = create_module(course_id=course.id, title='Mod2')

    # Register and login a student
    client.post('/register', json={'email': 'stud@example.com', 'password': 'Pass1234', 'role': 'student'})
    login_resp = client.post('/login_jwt', json={'email': 'stud@example.com', 'password': 'Pass1234'})
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    # Attempt download without enrollment – should get 403
    resp = client.get(f'/courses/{course.id}/modules/{module.id}/materials/sample.pdf', headers=headers)
    assert resp.status_code == 403

    # Enroll the student (using existing endpoint)
    client.post(f'/courses/{course.id}/enroll', headers=headers)

    # Now the download should succeed (file may not exist, expect 404 or 200 if fixture added)
    resp = client.get(f'/courses/{course.id}/modules/{module.id}/materials/sample.pdf', headers=headers)
    assert resp.status_code in (200, 404)
