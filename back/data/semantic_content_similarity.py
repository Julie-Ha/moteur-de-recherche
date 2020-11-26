import json
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import collections
import jsonpickle

def getLeafNodes(entity, nb):
    with open('ontology.csv') as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            if row[1] == entity:
                nb = getLeafNodes(row[0], nb+1)

    return nb
    
def getNbSubEntities(entity):
    nb = getLeafNodes(entity, 0)
  
    return nb



def getPc(nbSubEntities, N):
    return nbSubEntities/N

N = getNbSubEntities('entity')
nb = getNbSubEntities('person')
pc = getPc(nb, N)

print(nb)
print(pc)


