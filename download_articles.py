from scraper import *
import preprocess
from sys import argv
import yaml
import index

# Main script
if __name__ == '__main__':
    if "scrape" in argv:
        with open('sites.yaml', 'rb') as file:
            pages = yaml.load(file)

            Scraper(pages).downloadarticlesforeverywebsite()

    if 'lemmatize' in argv:
        preprocess.lemmatize()

    if 'index' in argv:
        index.index()
