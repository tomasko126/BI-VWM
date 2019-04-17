import json
import os
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter


def lemmatize():
    counter = 0
    articles = dict()

    for item in os.listdir('plain_articles'):
        counter = counter + 1
        articles.update({int(counter): item})

    with open('analyzed/_indexedArticles.json', 'w') as listF:
        json.dump(articles, listF, ensure_ascii=False)

    lemmatizer = WordNetLemmatizer()

    for file in os.listdir('plain_articles'):
        with open('plain_articles/'+file, 'r') as reader:
            try:
                text = reader.read().lower()

                text = re.sub(r'[^a-z ]', '', text)
                tokens = word_tokenize(text)

                words = list()
                [words.append(lemmatizer.lemmatize(x)) for x in tokens if x not in stopwords.words('english')]
                result = Counter(words)

                with open('analyzed/' + file + ".json", 'w') as writer:
                    json.dump(result, writer)
            except UnicodeDecodeError:
                if file == '.DS_Store':
                    continue
                else:
                    raise
