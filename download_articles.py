from scraper import *
import preprocess
from sys import stdin
from sys import argv
import search
import yaml
import index

if __name__ == "__main__":
    if 'scrape' in argv:
        with open("sites.yaml", 'rb') as file:
            pages = yaml.load(file)
        Scraper(pages).downloadArticlesForEveryWebsite()

    if 'lemmatize' in argv:
        preprocess.lemmatize()

    if 'index' in argv:
        index.index()

    if 'search' in argv:
        for line in stdin:
            search.search()

