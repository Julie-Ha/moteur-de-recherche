import csv

f = open('ontology.json','a')

def searchSubEntity(entity, f):
    f.write('{ "name": "'+entity+'"')
    with open('ontology.csv') as file:
        reader = csv.reader(file, delimiter=',')

        f.write(',"children": [')
        for row in reader:
            if row[1] == entity:
                searchSubEntity(row[0], f)
        f.write("]")
                
    f.write("}")

        

entity = "entity"
searchSubEntity(entity,f)
f.close()
