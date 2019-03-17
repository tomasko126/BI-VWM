from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re
import json
import os

counter = 0
articles = dict()
for item in os.listdir('plain_articles'):
    counter = counter+1
    articles.update({int(counter) : item})
with open('analyzed/_list.json', 'w') as listF:
    json.dump(articles, listF, ensure_ascii=False)

lemmatizer = WordNetLemmatizer()
for file in os.listdir('plain_articles'):
    with open('plain_articles/'+file, 'r') as reader:
        text = reader.read().lower()
    text = re.sub(r'[^a-z ]', '', text)
    tokens = word_tokenize(text)
    words = list()
    [words.append(lemmatizer.lemmatize(x)) for x in tokens if x not in stopwords.words('english')]
    result = Counter(words)

    with open('analyzed/'+file+".json", 'w') as writer:
        json.dump(result, writer)
