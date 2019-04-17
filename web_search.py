import json


def getWordWithLowestDocId(words):
    word_with_lowest_id = list(words.keys())[0]
    lowest_doc_id = int(words.get(word_with_lowest_id).get("docIdOnCurrentIndex"))

    for word in words:
        if int(words.get(word).get("docIdOnCurrentIndex")) < lowest_doc_id:
            word_with_lowest_id = word
            lowest_doc_id = int(words.get(word).get("docIdOnCurrentIndex"))

    return {"word_with_lowest_id": word_with_lowest_id, "lowest_doc_id": lowest_doc_id }


def getWeightsVector(words, usedDocsIndexes):

    hashmap = {}

    i = 0

    for word in words:
        currentDocId = words.get(word).get("docIdOnCurrentIndex")

        if not hashmap.get(currentDocId):
            hashmap[currentDocId] = list()

        hashmap[currentDocId].append([i, currentDocId, words.get(word).get('data')[currentDocId]])
        i += 1

    vectorWithWeights = [0] * len(words)

    for docId in hashmap:
        if len(hashmap.get(docId)) < 2:
            continue

        for array in range(len(hashmap[docId])):
            indexInVector = hashmap[docId][array][0]
            vectorWithWeights[indexInVector] = [hashmap[docId][array][1], hashmap[docId][array][2]]

    return vectorWithWeights

with open("words_weight_per_doc_test.json", "r") as f:
    matrix = json.load(f)

    allMatchedVectors = list()
    docsIndexes = set()

    words = dict()
    words['forest'] = {"data": matrix.get('forest'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('forest'))[0], "canMoveIndex": True}
    words['mountain'] = {"data": matrix.get('mountain'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('mountain'))[0], "canMoveIndex": True}
    words['nature'] = {"data": matrix.get('nature'), "currentIndex": 0, "docIdOnCurrentIndex": list(matrix.get('nature'))[0], "canMoveIndex": True}

    while True:

        # get vector with weights
        vectorWithWeights = getWeightsVector(words, docsIndexes)

        if vectorWithWeights:
            allMatchedVectors.append(vectorWithWeights)

        print(allMatchedVectors)

        # Get word with lowest doc ID and increment that ID later
        wordStats = getWordWithLowestDocId(words)
        word_with_lowest_id = wordStats.get("word_with_lowest_id")
        lowest_doc_id = wordStats.get("lowest_doc_id")

        # We add every doc id we come across to our docsIndexes set
        docsIndexes.add(lowest_doc_id)

        words.get(word_with_lowest_id)['currentIndex'] = words.get(word_with_lowest_id).get('currentIndex') + 1
        words.get(word_with_lowest_id)['docIdOnCurrentIndex'] = list(matrix.get(word_with_lowest_id))[words.get(word_with_lowest_id)['currentIndex']]

        # todo: what if the lowest id cant be incremented anymore?
        # find word with the second lowest id and try to increment that one
        # words.get(word_with_lowest_doc_id).get("currentIndex") += 1
