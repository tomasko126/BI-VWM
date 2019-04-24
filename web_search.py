#!/usr/bin/env python3

import json
import sys
import os
import math
import datetime

from operator import itemgetter


# This function will takes weights of all words and returns a dictionary
# consisting of key-value pairs: docId - [word, its weight]
def getSingleWeightVectors(allWords, vectorOfNeededWords):
    allVectors = {}

    for neededWord in vectorOfNeededWords:
        docIdAndWeightPair = allWords.get(neededWord)

        for wordDocId in docIdAndWeightPair:

            if not allVectors.get(wordDocId):
                allVectors[wordDocId] = {}

            wordDocIdWeight = docIdAndWeightPair[wordDocId]
            allVectors[wordDocId][neededWord] = wordDocIdWeight

    return allVectors


def inversedIndexSearch():
    # Get the ID of the requested doc
    idOfRequestedDoc = sys.argv[1]

    # os.chdir("../../")
    # print(os.getcwd())

    # Open up doc with articleId - articleName key-value pairs
    with open('./analyzed/_indexedArticles.json', 'r') as indexedDocsFile:
        indexedDocFileContent = json.load(indexedDocsFile)

        # Get the article name of the requested doc
        requestedDocName = indexedDocFileContent.get(idOfRequestedDoc)

        with open('./analyzed/' + requestedDocName + '.json', 'r') as analyzedRequestedDocFile:
            # Get the analyzed part of the requested doc
            analyzedRequestedDocContent = json.load(analyzedRequestedDocFile)

            # Sort words in the requested doc by their count
            analyzedRequestedDocContent = sorted(analyzedRequestedDocContent.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

            # We are interested in first 10 most frequented words in the requested document
            analyzedRequestedDocContent = analyzedRequestedDocContent[0:5]

            with open('./words_weight_per_doc.json', 'r') as f:
                # Retrieve weights of words in all docs
                weights_of_words_in_all_docs = json.load(f)

                # Init vector of requested doc
                vector_of_requested_doc = {}

                # For every word in the requested doc,
                # create a vector consisting of the word and its weight in the requested doc
                for tuple in analyzedRequestedDocContent:
                    # Tuple is a pair of word-no of that word in the doc
                    vector_of_requested_doc[tuple[0]] = weights_of_words_in_all_docs.get(tuple[0]).get(idOfRequestedDoc)

                # Contains docId: [word, its weight]
                weights = getSingleWeightVectors(weights_of_words_in_all_docs, vector_of_requested_doc)

                # This list will include all sorted final vectors
                allVectors = []

                # Calculate cosine similarity between vector of a requested doc
                # and vector of the particular document
                for docId in weights:
                    vector_of_current_doc = weights.get(docId)

                    sum = 0
                    wij = 0
                    wiq = 0

                    for word in vector_of_requested_doc:
                        weightOfWord = vector_of_current_doc.get(word) or 0

                        sum += (vector_of_requested_doc.get(word) * weightOfWord)
                        wij += vector_of_requested_doc.get(word) ** 2
                        wiq += weightOfWord ** 2

                    result = sum / ((wij * wiq) ** (1/2))

                    #if math.acos(result) < 0.7:
                    allVectors.append([docId, result])

                allVectors = sorted(allVectors, key=itemgetter(1), reverse=True)

                JSON = {'docs': []}

                # Get first 11 results - the first one should have the same ID as the requested document
                for x in range(0, 11):
                    JSON.get('docs').append(allVectors[x])

                print(json.dumps(JSON, ensure_ascii=False))

def sequentialSearch():
    # Get the ID of the requested doc
    idOfRequestedDoc = sys.argv[1]

    # Open up doc with articleId - articleName key-value pairs
    with open('./analyzed/_indexedArticles.json', 'r') as indexedDocsFile:
        indexedDocFileContent = json.load(indexedDocsFile)

        # Get the article name of the requested doc
        requestedDocName = indexedDocFileContent.get(idOfRequestedDoc)

        with open('./analyzed/' + requestedDocName + '.json', 'r') as analyzedRequestedDocFile:
            # Get the analyzed part of the requested doc
            analyzedRequestedDocContent = json.load(analyzedRequestedDocFile)

            # Sort words in the requested doc by their count
            analyzedRequestedDocContent = sorted(analyzedRequestedDocContent.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

            # We are interested in first 20 most frequented words in the requested document
            analyzedRequestedDocContent = analyzedRequestedDocContent[0:5]

            with open('./words_weight_per_doc.json', 'r') as f:
                # Retrieve weights of words in all docs
                weights_of_words_in_all_docs = json.load(f)

                # Init vector of requested doc
                vector_of_requested_doc = {}

                # For every word in the requested doc,
                # create a vector consisting of the word and its weight in the requested doc
                for tuple in analyzedRequestedDocContent:
                    # Tuple is a pair of word-no of that word in the doc
                    vector_of_requested_doc[tuple[0]] = weights_of_words_in_all_docs.get(tuple[0])[str(idOfRequestedDoc)]

                allVectors = []

                for docId in indexedDocFileContent:
                    nameOfCurrentDoc = indexedDocFileContent[docId]

                    if nameOfCurrentDoc == '.DS_Store':
                        continue

                    with open('./analyzed/' + nameOfCurrentDoc + '.json', 'r') as analyzedCurrentDocFile:
                        analyzedCurrentDocContent = json.load(analyzedCurrentDocFile)

                        vector_of_current_doc = {}

                        for word in vector_of_requested_doc:
                            vector_of_current_doc[word] = weights_of_words_in_all_docs.get(word).get(str(docId)) or 0

                        sum = 0
                        wij = 0
                        wiq = 0

                        for word in vector_of_requested_doc:
                            weightOfWord = vector_of_current_doc.get(word)

                            sum += (vector_of_requested_doc.get(word) * weightOfWord)
                            wij += vector_of_requested_doc.get(word) ** 2
                            wiq += weightOfWord ** 2

                        # Sum can be zero, when no word from vector of requested doc is contained in the vector of current doc
                        if sum == 0:
                            continue

                        result = sum / ((wij * wiq) ** (1 / 2))

                        #if math.acos(result) < 0.7:
                        allVectors.append([docId, result])

                allVectors = sorted(allVectors, key=itemgetter(1), reverse=True)

                JSON = {'docs': []}

                # Get first 11 results - the first one should have the same ID as the requested document
                for x in range(0, 11):
                    JSON.get('docs').append(allVectors[x])

                print(json.dumps(JSON, ensure_ascii=False))

a = datetime.datetime.now()
inversedIndexSearch()
b = datetime.datetime.now()
c = b - a
print(int(c.total_seconds() * 1000))

a = datetime.datetime.now()
sequentialSearch()
b = datetime.datetime.now()
c = b - a
print(int(c.total_seconds() * 1000))