import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
        with open('data/ontology.csv') as file:
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
    with open('data/typeid_name_wordnet.json') as typeid_name_wordnet:
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
    with open('data/dimension_name.txt') as dimension_name:
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
    with open('data/article_vector.json') as article_vector:
        articles = json.load(article_vector)
        for (k, v) in articles.items():
            cos = cosine_similarity([queryVector],[v])
            if cos > 0:
                results[k] = float(cos[0][0])

    return results


                


