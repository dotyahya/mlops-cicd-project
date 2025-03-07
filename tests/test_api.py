import pytest
import sys
import os
import json
from api.app import app
from api.model import SentimentModel
from api.dataset import load_sample_data

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
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "ML Model API is running"
    assert json_data["status"] == "active"
    assert json_data["model"] == "sentiment_analysis"

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["model_loaded"] == True

def test_predict_endpoint(client):
    """Test the prediction endpoint"""
    test_data = {"text": "This is amazing!"}
    response = client.post('/predict',
                         data=json.dumps(test_data),
                         content_type='application/json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "sentiment" in json_data
    assert json_data["sentiment"] in ["positive", "negative"]

def test_model_training():
    """Test model training with sample data"""
    model = SentimentModel()
    X, y = load_sample_data()
    model.train(X, y)
    
    # Test prediction
    test_text = "This is great!"
    prediction = model.predict(test_text)
    assert prediction in [0, 1]

if __name__ == '__main__':
    pytest.main([__file__, "-v"])