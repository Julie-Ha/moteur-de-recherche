from flask import Flask, jsonify, request 
from flask_cors import CORS
import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import collections
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
    similarities = {k: v for k, v in sorted(similarities.items(), key=lambda item: item[1], reverse=True)}
    similarities = {k: similarities[k] for k in list(similarities)[:10]}

    articles = []
    for key, value in similarities.items():
        articles.append(Article(key, value))

    return jsonpickle.encode(articles, unpicklable=False)

#Supprime la string devant le . : computer_user.computer_scientist => computer_scientist
def entitiesFormate(entities):
    for i in range(0, len(entities)):
        if "." in entities[i]:
            entities[i] = entities[i].split(".")[1]
    return entities

#Cherche tous les sous entites des entites (seulement les feuilles de l'arbre)
def searchSubEntity(entities):
    subEntities = []
    def getLeafNodes(entity):
        with open('ontology.csv') as file:
            reader = csv.reader(file, delimiter=',')

            found = False
            for row in reader:
                if row[1] == entity:
                    found = True
                    getLeafNodes(row[0])
                    
            if not found:
                subEntities.append(entity)

    for entity in entities:
        getLeafNodes(entity)

    subEntities = entitiesFormate(subEntities)
        
    return subEntities

#Cherche les types wordnet de chaque entite selectionnee dans typeid_name_wordnet.json
def getWordnetType(entities):
    wordnetTypes = []
    with open('typeid_name_wordnet.json') as typeid_name_wordnet:
        wordnet = json.load(typeid_name_wordnet)
        
        for e in entities:
            for w in wordnet.values():
                if(e == w["name"]):
                    wordnetTypes.append(w["type"])
                    break
                    
    return wordnetTypes

#Construit le vector de requete avec les entites selectionees
def createQueryVector(wordnet):
    vector = []
    with open('dimension_name.txt') as dimension_name:
        lines = dimension_name.readlines()

        
        for line in lines:
            found = False
            for w in wordnet:
                if w == line.strip():
                    found = True
                    break
            if found:
                vector.append(1)
            else:
                vector.append(0)
                
    return vector

#Calcule la cosine similarity entre le QueryVector et chaque article
def getCosSimilarity(wordnetVector):
    results = dict()
    with open('article_vector.json') as article_vector:
        articles = json.load(article_vector)
        for (k, v) in articles.items():
            cos = cosine_similarity([wordnetVector],[v])
            if cos > 0:
                results[k] = round(cos[0][0],4)

    return results

class Article:
    def __init__(self, title, score):
        self.title = title
        self.score = score

if __name__ == "__main__":
    app.run()

