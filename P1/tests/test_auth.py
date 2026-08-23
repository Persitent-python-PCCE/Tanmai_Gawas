# tests/test_auth.py

import pytest
from app import create_app
from config.config import TestingConfig
from config.db import db
from models.user import User

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_v1_success(client):
    """Test v1 register endpoint"""
    resp = client.post('/auth/register', json={
        'full_name': 'Test User',
        'education': 'Test Education',
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'student'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['message'] == 'User created'

def test_register_v1_missing_fields(client):
    """Test v1 register with missing fields"""
    resp = client.post('/auth/register', json={'email': 'test@example.com'})
    assert resp.status_code == 400

def test_register_v2_success(client):
    """Test v2 register endpoint"""
    resp = client.post('/api/v2/auth/register', json={
        'full_name': 'Test User',
        'education': 'Test Education',
        'email': 'test2@example.com',
        'password': 'password123',
        'role': 'student'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['message'] == 'User created'
    assert 'user' in data
    assert data['user']['email'] == 'test2@example.com'

def test_register_v2_missing_fields(client):
    """Test v2 register with missing fields"""
    resp = client.post('/api/v2/auth/register', json={'email': 'test2@example.com'})
    assert resp.status_code == 400

def test_login_v1_success(client):
    """Test v1 login endpoint"""
    client.post('/auth/register', json={
        'full_name': 'Test User',
        'education': 'Test Education',
        'email': 'login@example.com',
        'password': 'pass1234',
        'role': 'student'
    })
    resp = client.post('/auth/login', json={
        'email': 'login@example.com',
        'password': 'pass1234'
    })
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'Logged in'
    assert 'token' in resp.get_json()

def test_login_v2_success(client):
    """Test v2 login endpoint"""
    client.post('/api/v2/auth/register', json={
        'full_name': 'Test User',
        'education': 'Test Education',
        'email': 'login2@example.com',
        'password': 'pass1234',
        'role': 'student'
    })
    resp = client.post('/api/v2/auth/login', json={
        'email': 'login2@example.com',
        'password': 'pass1234'
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['message'] == 'Logged in'
    assert 'token' in data
    assert 'user' in data
    assert data['user']['email'] == 'login2@example.com'

def test_login_failure(client):
    """Test login with invalid credentials"""
    resp = client.post('/api/v2/auth/login', json={
        'email': 'nosuch@example.com',
        'password': 'doesntmatter'
    })
    assert resp.status_code == 401
    assert 'error' in resp.get_json()

def test_me_endpoint(client):
    """Test /api/v2/auth/me endpoint"""
    client.post('/api/v2/auth/register', json={
        'full_name': 'Test User',
        'education': 'Test Education',
        'email': 'me@example.com',
        'password': 'pass1234',
        'role': 'instructor'
    })
    login_resp = client.post('/api/v2/auth/login', json={
        'email': 'me@example.com',
        'password': 'pass1234'
    })
    token = login_resp.get_json()['token']
    
    resp = client.get('/api/v2/auth/me', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['email'] == 'me@example.com'
    assert data['role'] == 'instructor'

def test_logout_endpoint(client):
    """Test /api/v2/auth/logout endpoint"""
    client.post('/api/v2/auth/register', json={
        'full_name': 'Test User',
        'education': 'Test Education',
        'email': 'logout@example.com',
        'password': 'pass1234',
        'role': 'student'
    })
    login_resp = client.post('/api/v2/auth/login', json={
        'email': 'logout@example.com',
        'password': 'pass1234'
    })
    token = login_resp.get_json()['token']
    
    resp = client.post('/api/v2/auth/logout', headers={'Authorization': f'Bearer {token}'})
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'Logged out'