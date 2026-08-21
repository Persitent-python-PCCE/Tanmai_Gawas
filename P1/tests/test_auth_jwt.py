import json
import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import create_app
from config.config import TestingConfig
from config.db import db
from utils.jwt_util import create_access_token

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

def register_user(client: FlaskClient, email: str, password: str, role: str = 'student'):
    return client.post('/register', json={'email': email, 'password': password, 'role': role})

def test_jwt_login_and_protected_route(client):
    # Register a user first
    resp = register_user(client, 'jwtuser@example.com', 'StrongPass1', 'student')
    assert resp.status_code == 201

    # Login via JWT endpoint
    resp = client.post('/login_jwt', json={'email': 'jwtuser@example.com', 'password': 'StrongPass1'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'token' in data
    token = data['token']

    # Access a protected route that uses _ensure_student (e.g., /courses/<id>/progress)
    # Assuming there is a route '/courses/1/progress' that requires student role
    protected = client.get('/courses/1/progress', headers={'Authorization': f'Bearer {token}'})
    # The actual implementation returns a placeholder JSON or similar; let's check status
    assert protected.status_code in (200, 404) # 404 is acceptable if course 1 doesn't exist, but 401 is not
