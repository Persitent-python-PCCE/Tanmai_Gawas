# tests/test_auth.py

import pytest
from app import create_app
from config.config import TestingConfig

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client

def test_register_success(client):
    resp = client.post('/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'role': 'student'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['message'] == 'User created'

def test_register_missing_fields(client):
    resp = client.post('/register', json={'email': 'test@example.com'})
    assert resp.status_code == 400

def test_login_success(client, monkeypatch):
    # Register first
    client.post('/register', json={
        'email': 'login@example.com',
        'password': 'pass1234',
        'role': 'student'
    })
    resp = client.post('/login', json={
        'email': 'login@example.com',
        'password': 'pass1234'
    })
    assert resp.status_code == 200
    assert resp.get_json()['message'] == 'Logged in'
