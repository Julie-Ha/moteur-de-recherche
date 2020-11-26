from flask import Flask, jsonify, request 
from flask_cors import CORS
import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import collections
import jsonpickle
import networkx as nx

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

@app.route('/path-length', methods=['POST'])
def pathLength():
    entities = request.json['entities']
    similarities = calculation(entities)
    
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

#Calcule la cosine similarity entre le queryVector et le vector chaque article
def getCosSimilarity(queryVector):
    results = dict()
    with open('article_vector.json') as article_vector:
        articles = json.load(article_vector)
        for (k, v) in articles.items():
            cos = cosine_similarity([queryVector],[v])
            if cos > 0:
                results[k] = float(round(cos[0][0], 4))

    return results

class Article:
    def __init__(self, title, score):
        self.title = title
        self.score = score

class node:
    
    def _init_(self,name=None,children=None):
        self.name = name
        if children is None:
            self.children = [] 
        else:
            self.children = children

    def getName(self):
        return self.name
    def getChildren(self):
        liste = []
        for i in self.children:
            liste.append(i.name)
        return liste
    
#Construction of tree through recursion            
class implementation:
    nodes=[]
    def buildnode(self,ob):
        
        node1= node()
        node1.name= ob['name']
        node1.children=[]
        if "children" in ob:
            for children in ob['children']:
                node1.children.append(self.buildnode(children))

        self.nodes.append(node1)
        return node1
    def getNodes(self):
        return self.nodes
    

def createGraph(nodes):
    G = nx.Graph()
    for i in nodes:
        G.add_node(i.name)
    for i in nodes:
        for j in i.children:
            G.add_edge(i.name, j.name)
    return G

##Tuka ne znam dali treba da se dodade 1 mislam deka ne, prashaj go
##utre profesorot
def calculatePathLen(path, entity1, entity2):
    #return nx.shortest_path_length(G, entity1, entity2)+1
    return path[entity1][entity2]+1
def calculateSimPath(pathlen):
    return 1/pathlen
    
##queryValue, documentValue
def calculateHighestValue(path, q, document):
    highest = 0
    
    for i in document:
        pathlen = calculatePathLen(path, q, i)
       
        simpathlen = calculateSimPath(pathlen)
        if simpathlen > highest:
            highest = simpathlen
    return highest

##Moyene des plus grandes valurs
def calculateMeanValue(path, query, document):
     liste =[]
     for q in query: 
         h = calculateHighestValue(path, q, document)
        
         liste.append(h)
    
     return (sum(liste) / len(liste))
        

def calculation(query):
    f=open("ontology.json")
    data=json.load(f)
    builder = implementation()
    builder.buildnode(data)

    nodes = builder.getNodes()

    G = createGraph(nodes)
    ##Tous le distance
    path = dict(nx.all_pairs_shortest_path_length(G))
    dicto = {}
    with open('article_typeid.json') as article_vector:
        articles = json.load(article_vector)
   
        for article in articles:
             score = round(calculateMeanValue(path, query, articles[article]), 4)
             
             dicto[article]=score

    return dicto

if __name__ == "__main__":
    app.run()

