import networkx as nx
import json

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
    
#Construction de l'arbre           
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

def getPathLen(G, entity1, entity2):
    return path[entity1][entity2]+1

def getSimPath(pathlen):
    return 1/pathlen
    
def getHighestValue(q, document):
    highest = 0
    
    for i in document:
        pathlen = getPathLen(G, q, i)
       
        simpathlen = getSimPath(pathlen)
        if simpathlen > highest:
            highest = simpathlen
    return highest

##Moyenne des plus grandes valeurs
def getMeanValue(query, document):
     liste =[]
     for q in query: 
         h = getHighestValue(q, document)
        
         liste.append(h)
    
     return (sum(liste) / len(liste))
        

def getPathLengthSimilarity(entities):
    dico = {}
    with open('data/article_typeid.json') as article_vector:
        articles = json.load(article_vector)
   
        for article in articles:
             score = getMeanValue(entities, articles[article])
             
             dico[article]=score

    return dico

        
f=open("data/ontology.json")
data=json.load(f)
builder = implementation()
builder.buildnode(data)

nodes = builder.getNodes()
G = createGraph(nodes)
path = dict(nx.all_pairs_shortest_path_length(G))






