import pytest
from app import create_app
from dao.material_dao import create_material
from dao.lesson_dao import create_lesson
from dao.module_dao import create_module
from dao.course_dao import create_course

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

def test_material_upload_download(client):
    # Setup course/module/lesson
    admin_hdr = register_and_login(client, 'adm2@example.com', 'Pass123', role='admin')
    from dao.user_dao import get_user_by_email
    admin = get_user_by_email('adm2@example.com')
    course = create_course(title='MatCourse', description='', instructor_id=admin.id)
    module = create_module(course_id=course.id, title='Mod1')
    lesson = create_lesson(module_id=module.id, title='Lesson1')
    # Upload a material file (simulate by creating a file on disk)
    import os, io
    filename = 'sample.txt'
    file_path = os.path.join('uploads', str(module.id), filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write('sample content')
    # Mark material in DB (assume create_material exists)
    create_material(module_id=module.id, file_path=file_path, file_type='txt', uploaded_by=admin.id)
    # Student logs in and attempts download (enrolled first)
    student_hdr = register_and_login(client, 'stud2@example.com', 'Pass123')
    # Enroll student
    client.post(f'/courses/{course.id}/enroll', headers=student_hdr)
    # Download
    resp = client.get(f'/courses/{course.id}/modules/{module.id}/materials/{filename}', headers=student_hdr)
    assert resp.status_code == 200
    assert resp.data == b'sample content'
