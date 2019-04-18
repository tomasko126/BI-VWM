import threading
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Scraper class intended for scraping website articles
class Scraper:
    noOfDownloadedArticles = 0
    maxNumberOfDownloadedArticles = 0

    def __init__(self, pages):
        self.pages = pages
        self.http = urllib3.PoolManager()
        self.http.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})

        pass

    # Initiate download of articles for every given website
    # This gets called from the download_articles.py file
    def downloadarticlesforeverywebsite(self):
        for website in self.pages['sites']:
            self.downloadwebsitearticles(website)

    # Download articles from a particular website
    def downloadwebsitearticles(self, website):
        Scraper.maxNumberOfDownloadedArticles += website['maxNumberOfDownloadedArticles']

        pageindex = 1

        while Scraper.noOfDownloadedArticles <= Scraper.maxNumberOfDownloadedArticles:
            threading.Thread(target=self.downloadarticlestext(website, pageindex)).start()
            pageindex += 1

        pass

    # Make request to a given URL
    def downloadarticlestext(self, website, page_num):
        page = self.http.request('GET', website['url'].format(page_num))

        soup = BeautifulSoup(page._body, 'lxml')
        articles = soup.findAll('article', recursive=True)

        for x in articles:
            if Scraper.noOfDownloadedArticles <= Scraper.maxNumberOfDownloadedArticles:
                threading.Thread(target=self.extract(x.find('a')['href'])).start()

    # Extract an article from a given URL
    def extract(self, url):
        page = self.http.request('GET', url)
        soup = BeautifulSoup(page._body, 'lxml')

        article = soup.find('div', {'class': 'entry-content'})
        title = soup.find('h1', {'class': 'entry-title'})

        try:
            # Try to store the downloaded article
            with open('plain_articles/' + str(title.text).replace('/', ''), 'w') as f:
                f.write(article.text)
                Scraper.noOfDownloadedArticles += 1
        except AttributeError:
            print(url)
