import pytest
from app import create_app
from flask import url_for
from dao.lesson_completion_dao import mark_completed
from dao.quiz_dao import submit_quiz_result

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

def register_and_login_jwt(client, email, password, role='student'):
    client.post('/register', json={'email': email, 'password': password, 'role': role})
    resp = client.post('/login_jwt', json={'email': email, 'password': password})
    token = resp.get_json()['token']
    return {'Authorization': f'Bearer {token}'}

def test_progress_aggregation(client):
    # Setup a student, a course with one module and one lesson
    headers = register_and_login_jwt(client, 'studprog@example.com', 'Pass1234')
    # Create course, module, lesson via existing endpoints (assuming they exist)
    # For simplicity, we will directly use DAOs (bypass HTTP)
    from dao.course_dao import create_course
    from dao.module_dao import create_module
    from dao.lesson_dao import create_lesson
    from dao.user_dao import create_user
    instructor = create_user(email='instprog@example.com', password_hash='hash', role='instructor')
    course = create_course(title='Test Course', description='desc', instructor_id=instructor.id)
    module = create_module(course_id=course.id, title='Module 1')
    lesson = create_lesson(module_id=module.id, title='Lesson 1')
    # Mark lesson as completed
    mark_completed(student_id=1, lesson_id=lesson.id)  # Assuming student_id=1 from JWT payload
    # Submit a quiz result (score 80)
    from dao.quiz_dao import create_quiz
    quiz = create_quiz(title='Quiz 1', course_id=course.id, instructor_id=2)
    submit_quiz_result(quiz_id=quiz.id, student_id=1, answers_dict={1:0}, score=80)

    # Call progress endpoint
    resp = client.get(f'/courses/{course.id}/progress', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    # Expected: lesson_pct = 1 (1/1), quiz_pct = 0.8, overall = 0.7*1 + 0.3*0.8 = 0.94 -> 94%
    assert data['completion_percent'] == 94.0
