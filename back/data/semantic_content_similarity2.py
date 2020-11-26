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
print(G.number_of_nodes())


print(nx.dfs_tree(G, "person"))



