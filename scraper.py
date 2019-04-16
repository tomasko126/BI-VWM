import threading
import urllib3

from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Scraper:
    noOfDownloadedArticles = 0
    maxNumberOfDownloadedArticles = 0

    def __init__(self, pages):
        self.pages = pages
        self.http = urllib3.PoolManager()
        self.http.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        pass

    def extract(self, url):
        page = self.http.request('GET', url)
        soup = BeautifulSoup(page._body, 'lxml')

        article = soup.find("div", {"class":"entry-content"})
        title = soup.find("h1", {"class":"entry-title"})

        try:
            with open("plain_articles/"+str(title.text).replace("/",""), 'w') as f:
                f.write(article.text)
                Scraper.noOfDownloadedArticles += 1
        except AttributeError:
            print(url)

    def downloadArticlesForEveryWebsite(self):
        for website in self.pages["sites"]:
            self.downloadWebsiteArticles(website)

    def downloadWebsiteArticles(self, website):
        Scraper.maxNumberOfDownloadedArticles += website["maxNumberOfDownloadedArticles"]

        pageIndex = 1

        while Scraper.noOfDownloadedArticles <= Scraper.maxNumberOfDownloadedArticles:
            threading.Thread(target=self.downloadArticlesText(website, pageIndex)).start()
            pageIndex += 1

        pass

    def downloadArticlesText(self, website, page_num):
        page = self.http.request('GET', website["url"].format(page_num))
        soup = BeautifulSoup(page._body, 'lxml')
        articles = soup.findAll("article", recursive=True)

        for x in articles:
            if Scraper.noOfDownloadedArticles <= Scraper.maxNumberOfDownloadedArticles:
                threading.Thread(target=self.extract(x.find("a")["href"])).start()