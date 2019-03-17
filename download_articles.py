from scraper import *
import yaml
print(__name__)
if __name__ == "__main__":

    with open("sites.yaml", 'rb') as file:
        pages = yaml.load(file)

    s = Scraper(pages).downloadArticles()

