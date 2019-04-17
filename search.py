import json


def search():
    with open('tf_weight.json', 'r') as f:
        matrix = json.load(f)

    print(matrix[input()])

    with open('analyzed/_indexedArticles.json', 'r') as t:
        doc = json.load(t)
        print(doc[input()])
