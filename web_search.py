import json
import sys
from operator import itemgetter

def getSingleWeightVectors(words):
    docIdsWithWeights = dict()

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

    # Get the ID of the requested doc
    idOfRequestedDoc = sys.argv[1]

    with open("analyzed/_indexedArticles.json", "r") as inxDocFile:
        indexedDocFileContent = json.load(inxDocFile)

        # Get the article name of the requested doc
        articleName = indexedDocFileContent.get(idOfRequestedDoc)

        with open("analyzed/" + articleName + ".json", "r") as analyzedRequestedDoc:
            # Get the analyzed part of the requested doc
            analyzedRequestedDocContent = json.load(analyzedRequestedDoc)

            with open("words_weight_per_doc.json", "r") as f:
                matrix = json.load(f)

                # TODO: fix ordering
                weights_of_words_in_requested_doc = dict()
                weights_of_words_in_all_docs = dict()

                for word in analyzedRequestedDocContent:
                    weights_of_words_in_requested_doc[word] = {"data": {idOfRequestedDoc: matrix.get(word)[str(idOfRequestedDoc)]}}
                    weights_of_words_in_all_docs[word] = {"data": matrix.get(word)}

                # Init vector of requested doc
                vector_of_requested_doc = [[idOfRequestedDoc, 0]] * len(weights_of_words_in_requested_doc)

                counter = 0
                for word in weights_of_words_in_requested_doc:
                    vector_of_requested_doc[counter] = [idOfRequestedDoc, weights_of_words_in_requested_doc[word].get('data')[str(idOfRequestedDoc)]]
                    counter += 1

                #words['forest'] = {"data": matrix.get('forest'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('forest'))[0]}
                #words['mountain'] = {"data": matrix.get('mountain'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('mountain'))[0]}
                #words['nature'] = {"data": matrix.get('nature'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('nature'))[0]}

                allMatchedVectors = list()

                weights = getSingleWeightVectors(weights_of_words_in_all_docs)

                for docId in weights:
                    constructedVector = [[0, 0]] * len(weights_of_words_in_all_docs)

                    for vector in weights[docId]:
                        constructedVector[vector[0]] = [docId, vector[1]]

                    allMatchedVectors.append(constructedVector)

                print(allMatchedVectors)

                # will include inner product
                result = dict()

                for vector in allMatchedVectors:
                    counter = 0
                    sum = 0
                    docId = 0

                    for item in vector:
                        sum += item[1] * vector_of_requested_doc[counter][1]
                        counter += 1
                        if item[0] != 0:
                            docId = item[0]

                    # docId = vector_of_requested_doc[0][0]
                    result[docId] = sum

                result = sorted(result.items(), key=itemgetter(1))
                result