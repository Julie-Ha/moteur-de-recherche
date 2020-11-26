import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import collections
import jsonpickle
import networkx as nx
import matplotlib.pyplot as plt
import math 

def cosineSimilarity():
    entities = ['entity']
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

def pathLength():
    entities = ['entity']
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

f=open("ontology.json")
data=json.load(f)
builder = implementation()
builder.buildnode(data)

nodes = builder.getNodes()

G = createGraph(nodes)

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
    
    ##Tous le distance
    path = dict(nx.all_pairs_shortest_path_length(G))
    dicto = {}
    with open('article_typeid.json') as article_vector:
        articles = json.load(article_vector)
   
        for article in articles:
             score = round(calculateMeanValue(path, query, articles[article]), 4)
             
             dicto[article]=score

    return dicto

nodes = builder.getNodes()


##Directed Graph so we can easily retrieve the lowest subsumer of two entities
def createDiGraph():
    diG = nx.DiGraph()
    for i in nodes:
        diG.add_node(i.name)
    for i in nodes:
        for j in i.children:
            diG.add_edge(i.name, j.name)
    return diG


## Each leaf frequency
def calculateLeafFrequency():
    dico = {}
    with open('article_typeid.json') as article_type:
        articles = json.load(article_type)

        for i in articles:
            for j in articles[i]:
                if j in dico:
                   
                    dico[j] = dico[j] +1
                else:
                    dico[j]=1
##Leafs that are not present in the documents but present in the 
    with open("typeid_name_wordnet.json") as wordnet:
        words = json.load(wordnet)
        for i in words:
            if i not in dico:
                 dico[i] = 0
              
            
    return dico

## Sum of all the frequncy

def frequency():
    sume =0
    for i in leafFrequency :
        sume = sume + leafFrequency[i]
    return sume


## Calculation of each concept frequency
def calculateAllConceptsFrequency():
    dictionary = {}
    for i in nodes:
        if i.name in leafFrequency:
            
            dictionary[i.name] = leafFrequency[i.name]
        else:
            for j in nx.descendants(graph, i.name):
                if j in leafFrequency:
                    if i.name in dictionary:
                        dictionary[i.name] += leafFrequency[j]
                    else:
                        dictionary[i.name] = leafFrequency[j]
                
    return dictionary
    
####Calculate probabilites of each node
#### en utilisant la formule (nb de subnodes) / total number of nodes
##

def calculateProbabilites():
    probabilites = {}
    for i in nodes:
        p = everyConceptFrequency[i.name]/N
        probabilites[i.name]=p
    return probabilites
    

## -log(probability)

def calculateInformationContentDico():
    informations = {}
    probabilites = calculateProbabilites()
    for i in probabilites:
        ## je suis pas sur ce qu'on fait qu'on un entite n'est pas present dans les articles
        if probabilites[i] > 0:
            informations[i] = abs(math.log(probabilites[i]))
        else:
            informations[i] = 0
    return informations



##Using the Resnik Method
def calculateSimilarity(e1, e2):
    tup = (e1, e2)
    if tup in lowestCommonAncestor:
        lca = lowestCommonAncestor[(e1, e2)]
    else:
        lca = lowestCommonAncestor[(e2, e1)]
    
    
    return informationContent[lca]


def calculateHighestValueContentS(q, document):
    highest = 0
    for i in document:
        similarity = calculateSimilarity(q, i)
        if similarity > highest:
            highest = similarity
    return highest

def calculateMeanValueContentS(query, document):
    liste = []
    for q in query:
        h= calculateHighestValueContentS(q, document)
        liste.append(h)
    return (sum(liste)/ len(liste))

def calculationContentSimilarity(query):

    dico = {}
    with open('article_typeid.json') as article_vector:
        articles = json.load(article_vector)

        for article in articles:
            score = calculateMeanValueContentS(query, articles[article])
            dico[article] = score
    return dico
    

graph = createDiGraph()

print(len(nx.descendants(graph, "person")))

leafFrequency = calculateLeafFrequency()
N = frequency()
everyConceptFrequency = calculateAllConceptsFrequency()

print(everyConceptFrequency["person"])

informationContent = calculateInformationContentDico()
lowestCommonAncestor = dict(nx.all_pairs_lowest_common_ancestor(graph))

query = ["capital", "urban_area.city", "company", "organization", "district", "ruler"]

dico = calculationContentSimilarity(query)
dico = {k: v for k, v in sorted(dico.items(), key=lambda item: item[1], reverse= True)}
##
for i in list(dico)[:10]:
    print (i, dico[i])

