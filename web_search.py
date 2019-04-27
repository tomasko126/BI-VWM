#!/usr/bin/env python3

import json
import sys
import os
import math
import datetime

from operator import itemgetter


class Search:
    # Constructor
    def __init__(self):
        self.maxSearchedTerms = 10

        with open('../../analyzed/_indexedArticles.json', 'r') as indexedDocsFile:
            self.indexedDocsContent = json.load(indexedDocsFile)

        with open('../../words_weight_per_doc.json', 'r') as wordsWeightPerDocFile:
            self.wordsWeightPerDocContent = json.load(wordsWeightPerDocFile)

    # This function will create key-value pairs of docId-[word, its weight]
    # of words defined in vectorOfNeededWords
    def getSingleWeightVectors(self, vectorOfNeededWords):
        allVectors = {}

        for neededWord in vectorOfNeededWords:
            docIdAndWeightPair = self.wordsWeightPerDocContent.get(neededWord)

            for wordDocId in docIdAndWeightPair:

                if not allVectors.get(wordDocId):
                    allVectors[wordDocId] = {}

                wordDocIdWeight = docIdAndWeightPair[wordDocId]
                allVectors[wordDocId][neededWord] = wordDocIdWeight

        return allVectors

    # Returns vector of a document specified by document name and ID
    def getDocumentVector(self, docName, docId, toSlice=False):
        with open('analyzed/' + docName + '.json', 'r') as analyzedRequestedDocFile:
            # Get the analyzed part of the requested doc
            analyzedRequestedDocContent = json.load(analyzedRequestedDocFile)

            # Sort words in the requested doc by their count
            analyzedRequestedDocContent = sorted(analyzedRequestedDocContent.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

            # We are interested in first 10 most frequented words in the requested document
            if toSlice:
                analyzedRequestedDocContent = analyzedRequestedDocContent[0:self.maxSearchedTerms]

            # Init vector of requested doc
            vectorOfRequestedDoc = {}

            # For every word in the requested doc,
            # create a vector consisting of the word and its weight in the requested doc
            for tuple in analyzedRequestedDocContent:
                # Tuple is a pair of word-no of that word in the doc
                vectorOfRequestedDoc[tuple[0]] = self.wordsWeightPerDocContent.get(tuple[0]).get(docId)

            return vectorOfRequestedDoc

    # Returns name of a document defined by its ID
    def getDocumentName(self, docId):

        # Get the article name of the requested doc
        requestedDocName = self.indexedDocsContent.get(docId)

        return requestedDocName

    # Calculates cosine similarity between vectors of requested and current document
    def calculateCosineSim(self, requestedDocVector, currentDocVector):
        sum = 0
        wij = 0
        wiq = 0

        for word in requestedDocVector:
            weightOfWord = currentDocVector.get(word) or 0

            sum += (requestedDocVector.get(word) * weightOfWord)
            wij += requestedDocVector.get(word) ** 2
            wiq += weightOfWord ** 2

        # Sum can be zero, when no word from vector of requested doc is contained in the vector of current doc
        if sum == 0:
            return False

        result = sum / ((wij * wiq) ** (1 / 2))

        return result

    # JSON-ify vectors
    def makeJSON(self, vectors):
        vectorsInJSON = {'docs': []}

        # Get 2. - 11. vector - the first one should have the same ID as the requested document
        for x in range(1, 11):
            vectorsInJSON.get('docs').append(vectors[x])

        return vectorsInJSON

    # Perform search with usage of inverted index
    def inversedIndexSearch(self, requestedDocId):
        os.chdir("../../")

        # Get name of the requested document
        requestedDocName = self.getDocumentName(requestedDocId)

        # Get vector of the requested document
        requestedDocVector = self.getDocumentVector(requestedDocName, requestedDocId, True)

        # Get key-value pairs of docId-[word, its weight]
        weights = self.getSingleWeightVectors(requestedDocVector)

        # This list will include all sorted similar documents to the requested document
        similarDocuments = []

        # Calculate cosine similarity between vector of a requested doc
        # and vector of the particular document
        for currentDocId in weights:

            # Get vector of the current document
            currentDocVector = weights.get(currentDocId)

            # Calculate cosine similarity
            cosineSimilarity = self.calculateCosineSim(requestedDocVector, currentDocVector)

            if not cosineSimilarity:
                continue

            similarDocuments.append([currentDocId, cosineSimilarity])

        # Sort list of similar documents
        similarDocuments = sorted(similarDocuments, key=itemgetter(1), reverse=True)

        # Export list of similar documents to JSON
        similarDocumentsInJSON = self.makeJSON(similarDocuments)

        # Print it out
        print(json.dumps(similarDocumentsInJSON, ensure_ascii=False))

    # Perform search without usage of inverted index
    def sequentialSearch(self, requestedDocId):
        os.chdir("../../")

        # Get name of the requested document
        requestedDocName = self.getDocumentName(requestedDocId)

        # Get vector of the requested document
        requestedDocVector = self.getDocumentVector(requestedDocName, requestedDocId, True)

        # This list will include all sorted similar documents to the requested document
        similarDocuments = []

        # Loop through every stored document, calculate its vector and
        # compare it with the vector of the requested document by cosine similarity
        for currentDocId in self.indexedDocsContent:
            currentDocName = self.getDocumentName(currentDocId)

            # Ignore macOS specific file
            if currentDocName == '.DS_Store':
                continue

            # Get vector of the current document
            currentDocVector = self.getDocumentVector(currentDocName, currentDocId)

            # Calculate cosine similarity
            cosineSimilarity = self.calculateCosineSim(requestedDocVector, currentDocVector)

            if not cosineSimilarity:
                continue

            similarDocuments.append([currentDocId, cosineSimilarity])

        # Sort list of similar documents
        similarDocuments = sorted(similarDocuments, key=itemgetter(1), reverse=True)

        # Export list of similar documents to JSON
        similarDocumentsInJSON = self.makeJSON(similarDocuments)

        # Print it out
        print(json.dumps(similarDocumentsInJSON, ensure_ascii=False))


search = Search()

if sys.argv[1] == "inverted":
    a = datetime.datetime.now()

    search.inversedIndexSearch(sys.argv[2])

    b = datetime.datetime.now()
    c = b - a
    print(int(c.total_seconds() * 1000))
elif sys.argv[1] == "sequential":
    a = datetime.datetime.now()

    search.sequentialSearch(sys.argv[2])

    b = datetime.datetime.now()
    c = b - a
    print(int(c.total_seconds() * 1000))
