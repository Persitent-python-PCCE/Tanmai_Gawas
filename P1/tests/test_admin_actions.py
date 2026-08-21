import pytest
from app import create_app
from config.config import TestingConfig
from config.db import db
from dao.user_dao import create_user, delete_user_by_id, get_all_users

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

def admin_headers(client):
    client.post('/register', json={'email':'adminx@example.com','password':'Pass1234','role':'admin'})
    resp = client.post('/login_jwt', json={'email':'adminx@example.com','password':'Pass1234'})
    token = resp.get_json()['token']
    return {'Authorization': f'Bearer {token}'}

def test_admin_user_management(client):
    hdr = admin_headers(client)
    # Create a normal user via DAO (bypass endpoint)
    user = create_user(email='normal@example.com', password_hash='hashed', role='student')
    # List users via admin endpoint
    resp = client.get('/admin/users', headers=hdr)
    assert resp.status_code == 200
    users = resp.get_json()
    assert any(u['email'] == 'normal@example.com' for u in users)
    # Delete the user via admin endpoint
    del_resp = client.delete(f'/admin/users/{user.id}', headers=hdr)
    assert del_resp.status_code == 200
    # Verify removal
    remaining = get_all_users()
    assert all(u.id != user.id for u in remaining)
