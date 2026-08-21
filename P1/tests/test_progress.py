import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_progress_endpoint_requires_student(client):
    # Register a student and login via JWT
    client.post('/register', json={'email': 'stud2@example.com', 'password': 'Pass1234', 'role': 'student'})
    login_resp = client.post('/login_jwt', json={'email': 'stud2@example.com', 'password': 'Pass1234'})
    token = login_resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    # Access progress endpoint
    resp = client.get('/courses/1/progress', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'completion_percent' in data
