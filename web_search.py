import json
import sys
from operator import itemgetter


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


if __name__ == '__main__':

    # Get the ID of the requested doc
    idOfRequestedDoc = sys.argv[1]

    # Open up doc with articleId - articleName key-value pairs
    with open('analyzed/_indexedArticles.json', 'r') as indexedDocsFile:
        indexedDocFileContent = json.load(indexedDocsFile)

        # Get the article name of the requested doc
        articleName = indexedDocFileContent.get(idOfRequestedDoc)

        with open('analyzed/' + articleName + '.json', 'r') as analyzedRequestedDocFile:
            # Get the analyzed part of the requested doc
            analyzedRequestedDocContent = json.load(analyzedRequestedDocFile)

            with open('words_weight_per_doc.json', 'r') as f:
                # Retrieve weights of words in all docs
                weights_of_words_in_all_docs = json.load(f)

                # Init vector of requested doc
                vector_of_requested_doc = {}

                # For every word in the requested doc,
                # create a vector consisting of the word and its weight in the requested doc
                for word in analyzedRequestedDocContent:
                    vector_of_requested_doc[word] = weights_of_words_in_all_docs.get(word)[str(idOfRequestedDoc)]

                # TODO: Use merge-sort style of processing inverted index
                # Contains docId: [word, its weight]
                weights = getSingleWeightVectors(weights_of_words_in_all_docs, vector_of_requested_doc)

                # This list will include all sorted final vectors
                allVectors = []

                for docId in weights:
                    wordsInDocId = weights.get(docId)

                    sum = 0
                    wij = 0
                    wiq = 0

                    for word in wordsInDocId:
                        weightOfWord = wordsInDocId.get(word)

                        sum += (vector_of_requested_doc.get(word) * weightOfWord)
                        wij += vector_of_requested_doc.get(word) ** 2
                        wiq += weightOfWord ** 2

                    result = sum / ((wij * wiq) ** (1/2))
                    allVectors.append([docId, result])

                allVectors = sorted(allVectors, key=itemgetter(1), reverse=True)

                JSON = {'docs': []}

                # We exclude the first vector, because it has got the same ID
                # as the requested doc
                for x in range(1, 11):
                    JSON.get('docs').append(allVectors[x])

                print(json.dumps(JSON, ensure_ascii=False))