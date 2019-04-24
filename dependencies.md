# list of dependencies
- Python3.6 or higher
- PyYaml		5.1
- BeautifulSoup4	4.7.1
- lxml		4.3.2
- ntlk		3.4
- numpy		1.16
- urllib3		1.24

## run with python download_articles.py 
possible arguments :
 - scrape
 - lemmatize
 - index
 - search
 
 # Output:
 `vector of keywords with relative frequency per document (if the keyword occured)
 
 # More websites
  The scraper takes sites from sites.yaml where similar blogs are in comment block.
  If you want to scrape more blogs, add them with same structure with page list bounds and also with
  target css class, also scraper.py must be edited a bit.
