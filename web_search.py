import json
import sys

def getSingleWeightVectors(words):
    docIdsWithWeights = dict()

    singleWeightVectors = [0] * len(words)

    counter = 0
    for word in words:
        wordKeys = list(words.get(word).get('data').keys())
        wordValues = list(words.get(word).get('data').values())

        keysCounter = 0
        for x in wordKeys:
            docId = int(x)
            docIdWeight = wordValues[keysCounter]

            if not docIdsWithWeights.get(docId):
                docIdsWithWeights[docId] = list()

            docIdsWithWeights[docId].append([counter, docIdWeight])

            keysCounter += 1

        counter += 1

    return docIdsWithWeights


if __name__ == "__main__":

    idOfRequestedDoc = sys.argv[1]

    with open("analyzed/_indexedArticles.json", "r") as inxArtsFile:
        indexedArticlesFileContent = json.load(inxArtsFile)

        articleName = indexedArticlesFileContent.get(idOfRequestedDoc)

        with open("analyzed/" + articleName + ".json", "r") as analyzedRequestedDoc:
            analyzedRequestedDocContent = json.load(analyzedRequestedDoc)

            with open("words_weight_per_doc_test.json", "r") as f:
                matrix = json.load(f)

                # TODO: fix ordering
                words = dict()
                words['forest'] = {"data": matrix.get('forest'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('forest'))[0]}
                words['mountain'] = {"data": matrix.get('mountain'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('mountain'))[0]}
                words['nature'] = {"data": matrix.get('nature'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('nature'))[0]}

                allMatchedVectors = list()

                weights = getSingleWeightVectors(words)

                for docId in weights:
                    constructedVector = [[0, 0]] * len(words)

                    for vector in weights[docId]:
                        constructedVector[vector[0]] = [docId, vector[1]]

                    allMatchedVectors.append(constructedVector)

                print(allMatchedVectors)