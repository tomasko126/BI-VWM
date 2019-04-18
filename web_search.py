import json
import sys
from operator import itemgetter


def getSingleWeightVectors(words):
    allVectors = {}

    counter = 0
    for word in words:
        wordInDocsId = list(words.get(word).keys())
        wordWeightInDocsId = list(words.get(word).values())

        keysCounter = 0
        for docId in wordInDocsId:
            docId = int(docId)
            docIdWeight = wordWeightInDocsId[keysCounter]

            if not allVectors.get(docId):
                allVectors[docId] = {}

            allVectors[docId][word] = docIdWeight

            keysCounter += 1

        counter += 1

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

                # TODO: Do NOT use this, use merge-sort style of processing inverted index
                # Contains docId: [word, its weight]
                weights = getSingleWeightVectors(weights_of_words_in_all_docs)

                # TODO: Reword everything below
                # will include inner product
                result = dict()

                for vector in weights:
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