import json
import os

def index():
    matrice = dict()
    with open('analyzed/_list.json', 'r') as f:
        articles = json.load(f)

    print(articles)
    print(os.path.isfile('analyzed/'+articles[str(2)]+'.json'))
    for x in articles:
        with open('analyzed/'+articles[x]+'.json', 'r') as f:
            doc_dict = json.load(f)
        most_occurences =  max(doc_dict.values())
        for y in doc_dict:
            doc_dict[y] = doc_dict[y]/most_occurences
            if y not in matrice.keys():
                matrice.update({y: dict()})
            matrice[y].update({x: doc_dict[y]})
    with open('test.json', 'w') as f:
        json.dump(matrice, f)
