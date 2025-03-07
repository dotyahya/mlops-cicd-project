import pytest
from api.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home route (/)"""
    response = client.get('/') # GET request
    assert response.status_code == 200 # STATUS OK
    json_data = response.get_json()
    assert json_data["message"] == "basic ci/cd pipeline setup for project"
    assert json_data["status"] == "green"