import pytest
import sys
import os

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("PYTHONPATH:", os.environ.get('PYTHONPATH', ''))
print("Contents of current directory:", os.listdir('.'))

try:
    from api.app import app
    print("Successfully imported app")
except Exception as e:
    print("Error importing app:", str(e))
    raise

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_basic():
    """Basic test to ensure testing works"""
    print("Running basic test")
    assert True

def test_addition():
    """Basic math test"""
    print("Running addition test")
    assert 1 + 1 == 2

def test_home_endpoint(client):
    """Test the home route (/)"""
    print("Running home endpoint test")
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "basic ci/cd pipeline setup for project"
    assert json_data["status"] == "green"

if __name__ == '__main__':
    pytest.main([__file__, "-v"])