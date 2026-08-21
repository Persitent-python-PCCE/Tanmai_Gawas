import pytest
from app import create_app

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

def register_and_login(client, email, password, role='student'):
    client.post('/register', json={'email': email, 'password': password, 'role': role})
    resp = client.post('/login_jwt', json={'email': email, 'password': password})
    token = resp.get_json()['token']
    return {'Authorization': f'Bearer {token}'}

def test_enrollment_flow(client):
    # Create a course via admin API (assume admin user exists)
    admin_headers = register_and_login(client, 'admin@example.com', 'AdminPass1', role='admin')
    # Create course
    resp = client.post('/admin/courses/create', data={'title': 'EnrollCourse', 'description': ''}, headers=admin_headers)
    assert resp.status_code in (200, 302)
    # Get course list to find ID
    resp = client.get('/courses', headers=admin_headers)
    courses = resp.get_json()['courses']
    course_id = next(c['id'] for c in courses if c['title'] == 'EnrollCourse')
    # Register a student and enroll
    student_headers = register_and_login(client, 'student@example.com', 'StudPass1')
    enroll_resp = client.post(f'/courses/{course_id}/enroll', headers=student_headers)
    assert enroll_resp.status_code == 302  # redirect after flash
    # Verify enrollment appears in my enrollments page
    resp = client.get('/my/enrollments', headers=student_headers)
    assert resp.status_code == 200
    assert 'EnrollCourse' in resp.get_data(as_text=True)
    # Unenroll
    unenroll_resp = client.post(f'/courses/{course_id}/unenroll', headers=student_headers)
    assert unenroll_resp.status_code == 302
    # Verify removed
    resp = client.get('/my/enrollments', headers=student_headers)
    assert 'EnrollCourse' not in resp.get_data(as_text=True)
