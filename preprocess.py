import json
import os
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Lemmatize all downloaded articles
def lemmatize():
    counter = 0
    articles = dict()

    # Load up every article into dictionary
    for item in os.listdir('plain_articles'):
        counter += 1
        articles.update({int(counter): item})

    with open('analyzed/_indexedArticles.json', 'w') as listF:
        json.dump(articles, listF, ensure_ascii=False)

    # Init lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Open up every downloaded article and lemmatize it
    for file in os.listdir('plain_articles'):
        with open('plain_articles/' + file, 'r') as reader:
            try:
                text = reader.read().lower()

                # Remove unwanted chars
                text = re.sub(r'[^a-z ]', '', text)
                tokens = word_tokenize(text)

                # Remove unwanted words
                words = list()
                [words.append(lemmatizer.lemmatize(x)) for x in tokens if x not in stopwords.words('english')]

                result = Counter(words)

                # Store the result
                with open('analyzed/' + file + '.json', 'w') as writer:
                    json.dump(result, writer)
            except UnicodeDecodeError:
                if file == '.DS_Store':
                    continue
                else:
                    raise
