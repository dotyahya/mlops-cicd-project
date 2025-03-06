from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
            "message": "basic ci/cd pipeline setup for project", 
            "status": "green"
        })

if __name__ == '__main__':
    app.run()
