import pytest
from app import create_app
from config.config import TestingConfig
from flask import url_for
from dao.user_dao import get_user_by_email
from config.db import db

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_success(client):
    resp = client.post('/auth/register', json={
        'email': 'user1@example.com',
        'password': 'strongpass',
        'role': 'student'
    })
    assert resp.status_code == 201
    assert resp.get_json()['message'] == 'User created'
    # verify user in DB
    user = get_user_by_email('user1@example.com')
    assert user is not None
    assert user.role == 'student'

def test_register_duplicate(client):
    # first registration
    client.post('/auth/register', json={
        'email': 'dup@example.com',
        'password': 'strongpass',
        'role': 'student'
    })
    # duplicate
    resp = client.post('/auth/register', json={
        'email': 'dup@example.com',
        'password': 'another',
        'role': 'student'
    })
    assert resp.status_code == 400
    assert 'error' in resp.get_json()

def test_login_success(client):
    # register user first
    client.post('/auth/register', json={
        'email': 'login@example.com',
        'password': 'pass1234',
        'role': 'instructor'
    })
    resp = client.post('/auth/login', json={
        'email': 'login@example.com',
        'password': 'pass1234'
    })
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'Logged in'

def test_login_failure(client):
    resp = client.post('/auth/login', json={
        'email': 'nosuch@example.com',
        'password': 'doesntmatter'
    })
    assert resp.status_code == 401
    assert 'error' in resp.get_json()

def test_admin_protected_route(client):
    # register admin
    client.post('/auth/register', json={
        'email': 'admin@example.com',
        'password': 'adminpass',
        'role': 'admin'
    })
    # login admin
    client.post('/auth/login', json={
        'email': 'admin@example.com',
        'password': 'adminpass'
    })
    # access protected admin route
    resp = client.get('/admin-only')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'Hello admin' in data['message']
