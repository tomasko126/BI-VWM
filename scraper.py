import urllib3
from bs4 import BeautifulSoup
import threading
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Scraper:
    def __init__(self, pages):
        self.pages = pages
        self.http = urllib3.PoolManager()
        self.http.headers.update({ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        pass

    def downloadArticles(self):
        for website in self.pages["sites"]:
            self.download(website)

    def extract(self, url):
        page = self.http.request('GET', url)
        soup = BeautifulSoup(page._body, 'lxml')

        article = soup.find("div", {"class":"entry-content"})
        title = soup.find("h1", {"class":"entry-title"})
        try:
            with open("plain_articles/"+str(title.text).replace("/",""), 'w') as f:
                f.write(article.text)
        except AttributeError:
            print(url)

    def downloadArticlesText(self, website, page_num):
        page = self.http.request('GET', website["url"].format(page_num))
        soup = BeautifulSoup(page._body, 'lxml')
        articles = soup.findAll("article", recursive=True)
        for x in articles:
            threading.Thread(target=self.extract(x.find("a")["href"])).start()

    def download(self, website):
        for x in range(website["min"], website["max"]):
            threading.Thread(target=self.downloadArticlesText(website, x)).start()

        pass

