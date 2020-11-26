from flask import Flask, jsonify, request 
from flask_cors import CORS
from cosine_similarity import *
from pathlength_similarity import *
from semantic_content_similarity import *
import jsonpickle

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return "hello world"

@app.route('/cosine-similarity', methods=['POST'])
def cosineSimilarity():
    entities = request.json['entities']
    entities = searchSubEntity(entities)
    wordnetTypes = getWordnetType(entities)
    wordnetVector = createQueryVector(wordnetTypes)

    similarities = getCosSimilarity(wordnetVector)

    return getJSONArticlesScore(similarities)

@app.route('/path-length', methods=['POST'])
def pathLengthSimilarity():
    entities = request.json['entities']
    similarities = getPathLengthSimilarity(entities)
    
    return getJSONArticlesScore(similarities)

@app.route('/semantic-content', methods=['POST'])
def semanticContentSimilarity():
    entities = request.json['entities']
    similarities = getInformationContentSimilarity(entities)
    
    return getJSONArticlesScore(similarities)
  
def getJSONArticlesScore(similarities):
    similarities = {k: v for k, v in sorted(similarities.items(), key=lambda item: item[1], reverse=True)}
    similarities = {k: similarities[k] for k in list(similarities)[:10]}

    articles = []
    for key, value in similarities.items():
        articles.append(Article(key, value))

    return jsonpickle.encode(articles, unpicklable=False)

class Article:
    def __init__(self, title, score):
        self.title = title
        self.score = round(score, 4)

if __name__ == "__main__":
    app.run()
