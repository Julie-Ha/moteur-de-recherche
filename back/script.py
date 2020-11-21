from flask import Flask, jsonify, request 
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "hello world"

@app.route('/cosine-similarity', methods=['POST'])
def cosineSimilarity():
    return jsonify(request.json['entities'])

if __name__ == "__main__":
    app.run()