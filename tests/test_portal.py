import pytest
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use a test submissions file
    import app as app_module
    app_module.SUBMISSIONS_FILE = "test_submissions.json"
    with app.test_client() as client:
        yield client
    # Cleanup
    if os.path.exists("test_submissions.json"):
        os.remove("test_submissions.json")

# TEST CASE 1: Complete details and valid URL — should be saved
def test_valid_submission(client):
    response = client.post('/submit',
        data=json.dumps({
            "name": "Ali Hassan",
            "reg_number": "FA21-BSE-001",
            "title": "DevOps Lab Assignment",
            "url": "https://github.com/ali/devops-lab"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['success'] == True

    # Verify it appears in the submission list
    list_response = client.get('/submissions')
    submissions = json.loads(list_response.data)
    assert any(s['reg_number'] == 'FA21-BSE-001' for s in submissions)

# TEST CASE 2: Missing registration number — should be rejected
def test_missing_registration_number(client):
    response = client.post('/submit',
        data=json.dumps({
            "name": "Sara Khan",
            "reg_number": "",
            "title": "DevOps Lab",
            "url": "https://github.com/sara/lab"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] == False
    assert 'registration' in data['message'].lower() or 'required' in data['message'].lower()

# TEST CASE 3: Invalid URL — should be rejected and not saved
def test_invalid_url(client):
    response = client.post('/submit',
        data=json.dumps({
            "name": "Omar Farooq",
            "reg_number": "FA21-BSE-002",
            "title": "My Assignment",
            "url": "not-a-valid-url"
        }),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['success'] == False

    # Make sure it was NOT saved
    list_response = client.get('/submissions')
    submissions = json.loads(list_response.data)
    assert not any(s['reg_number'] == 'FA21-BSE-002' for s in submissions)