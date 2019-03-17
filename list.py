import json
with open('test.json', 'r') as f:
    matrice = json.load(f)
print(matrice)
print(matrice[input()])
with open('analyzed/_list.json', 'r') as t:
    doc = json.load(t)
    print(doc[input()])