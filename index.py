import json
import os
import math


def index():
    NO_OF_DOCS = 1000

    matrix_tf = dict()
    matrix_word_frequency = dict()
    matrix_word_weights = dict()
    
    with open('analyzed/_indexedArticles.json', 'r') as f:
        articles = json.load(f)

    # print(articles)
    # print(os.path.isfile('analyzed/' + articles[str(2)] + '.json'))

    for articleIndex in articles:
        if articles[articleIndex] == '.DS_Store':
            continue

        with open('analyzed/' + articles[articleIndex] + '.json', 'r') as f:
            article_words = json.load(f)

        # Find word with most occurrence in the current document
        most_occurrence = max(article_words.values())

        for word in article_words:

            # Calculating tf of a word in a particular document
            tf_of_word = article_words[word]/most_occurrence

            if word not in matrix_tf.keys():
                matrix_tf.update({word: dict()})
            matrix_tf[word].update({articleIndex: tf_of_word})

            # Store document frequency of a particular term
            if word not in matrix_word_frequency.keys():
                matrix_word_frequency.update({word: 1})
            else:
                matrix_word_frequency.update({word: matrix_word_frequency[word] + 1})

    # Calculate idf and weight of word
    for word in matrix_tf.keys():

        for docId in matrix_tf.get(word):

            tf_of_word = matrix_tf.get(word).get(docId)
            no_of_docs_containing_word = matrix_word_frequency.get(word)

            idf_of_word = math.log(NO_OF_DOCS / no_of_docs_containing_word, 2)

            weight_of_word = tf_of_word * idf_of_word

            matrix_tf[word][docId] = weight_of_word

    with open('words_total_frequency.json', 'w') as f:
        json.dump(matrix_word_frequency, f)

    with open('words_weight_per_doc.json', 'w') as f:
        json.dump(matrix_tf, f)
