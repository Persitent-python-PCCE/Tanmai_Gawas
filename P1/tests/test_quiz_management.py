import pytest
from app import create_app
from dao.quiz_dao import create_quiz, submit_quiz_result
from dao.course_dao import create_course
from dao.module_dao import create_module

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

def register_and_login(client, email, password, role='instructor'):
    client.post('/register', json={'email': email, 'password': password, 'role': role})
    resp = client.post('/login_jwt', json={'email': email, 'password': password})
    token = resp.get_json()['token']
    return {'Authorization': f'Bearer {token}'}

def test_quiz_creation_and_attempt(client):
    # Setup course & module
    admin_hdr = register_and_login(client, 'instr@example.com', 'Pass123', role='instructor')
    from dao.user_dao import get_user_by_email
    instructor = get_user_by_email('instr@example.com')
    course = create_course(title='QuizCourse', description='', instructor_id=instructor.id)
    module = create_module(course_id=course.id, title='Mod')
    # Create a quiz via DAO
    quiz = create_quiz(title='Test Quiz', course_id=course.id, instructor_id=instructor.id)
    # Submit a result for a student
    student_hdr = register_and_login(client, 'stud3@example.com', 'Pass123', role='student')
    client.post(f'/courses/{course.id}/enroll', headers=student_hdr)
    student = get_user_by_email('stud3@example.com')
    result = submit_quiz_result(quiz_id=quiz.id, student_id=student.id, answers_dict={1:0}, score=85)
    assert result.score == 85
    # Verify quiz appears in list endpoint (assuming exists)
    resp = client.get(f'/courses/{course.id}/quizzes', headers=student_hdr)
    assert resp.status_code == 200
    quizzes = resp.get_json()
    assert any(q['title'] == 'Test Quiz' for q in quizzes)
