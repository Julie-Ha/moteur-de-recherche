from  pathlength_similarity  import *
import matplotlib.pyplot as plt
import math 


nodes = builder.getNodes()


#Construit le Directed Graph pour retrouver la sous entite d'une entite
def createDiGraph():
    diG = nx.DiGraph()
    for i in nodes:
        diG.add_node(i.name)
    for i in nodes:
        for j in i.children:
            diG.add_edge(i.name, j.name)
    return diG

#Calcule la frequence d'une entite
def getEntitiesFrequency():
    dico = {}
    with open('data/article_typeid.json') as article_type:
        articles = json.load(article_type)

        for i in articles:
            for j in articles[i]:
                if j in dico:
                   
                    dico[j] = dico[j] +1
                else:
                    dico[j]=1
                    
#Les entites qui ne sont pas presentes mais qui le sont dans typeid_name_wordnet
    with open("data/typeid_name_wordnet.json") as wordnet:
        words = json.load(wordnet)
        for i in words:
            if i not in dico:
                 dico[i] = 0
              
            
    return dico

#Somme les frequences
def frequency():
    f = 0
    for i in entitiesFrequency :
        f = f + entitiesFrequency[i]
    return f


def getAllConceptsFrequency():
    dictionary = {}
    for i in nodes:
        if i.name in entitiesFrequency:
            
            dictionary[i.name] = entitiesFrequency[i.name]
        else:
            for j in nx.descendants(graph, i.name):
                if j in entitiesFrequency:
                    if i.name in dictionary:
                        dictionary[i.name] += entitiesFrequency[j]
                    else:
                        dictionary[i.name] = entitiesFrequency[j]
                
    return dictionary
    
#Calcule la probabilite P(c)
def getProbabilities():
    probabilities = {}
    for i in nodes:
        p = everyConceptFrequency[i.name]/N
        probabilities[i.name]=p
    return probabilities
    

#Calcule -log P(c)
def getInformationContent():
    informations = {}
    probabilities = getProbabilities()
    for i in probabilities:
        if probabilities[i] > 0:
            informations[i] = abs(math.log(probabilities[i]))
        else:
            informations[i] = 0
    return informations



#Resnik Method
def getSimilarity(e1, e2):
    tup = (e1, e2)
    if tup in lowestCommonAncestor:
        lca = lowestCommonAncestor[(e1, e2)]
    else:
        lca = lowestCommonAncestor[(e2, e1)]
    
    
    return informationContent[lca]


def getHighestValueContent(q, document):
    highest = 0
    for i in document:
        similarity = getSimilarity(q, i)
        if similarity > highest:
            highest = similarity
    return highest

def getMeanValueContent(query, document):
    liste = []
    for q in query:
        h= getHighestValueContent(q, document)
        liste.append(h)
    return (sum(liste)/ len(liste))

def getInformationContentSimilarity(entities):

    dico = {}
    with open('data/article_typeid.json') as article_vector:
        articles = json.load(article_vector)

        for article in articles:
            score = getMeanValueContent(entities, articles[article])
            dico[article] = score
    return dico
    

graph = createDiGraph()
entitiesFrequency = getEntitiesFrequency()
N = frequency()
everyConceptFrequency = getAllConceptsFrequency()
informationContent = getInformationContent()
lowestCommonAncestor = dict(nx.all_pairs_lowest_common_ancestor(graph))







