from flask import Flask, jsonify, request
from .model import SentimentModel
from .dataset import load_sample_data

app = Flask(__name__)
model = SentimentModel()

# Train the model on startup
X, y = load_sample_data()
model.train(X, y)

@app.route('/')
def home():
    return jsonify({
        "message": "ML Model API is running",
        "status": "active",
        "model": "sentiment_analysis"
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    prediction = model.predict(data['text'])
    return jsonify({
        "text": data['text'],
        "sentiment": "positive" if prediction == 1 else "negative"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
