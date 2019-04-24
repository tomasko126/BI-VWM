# List of dependencies
- ```Python 3.6 or higher```
- ```PyYaml 5.1```
- ```BeautifulSoup4 4.7.1```
- ```lxml 4.3.2```
- ```ntlk 3.4```
- ```numpy 1.16```
- ```urllib3 1.24```

# Run from CLI

## Preprocessing
In order to preprocess the articles, the following command is available with further arguments:

```python3 download_articles.py <args>```

Possible arguments:
 - ```scrape```
 - ```lemmatize```
 - ```index```
 
 ```scrape``` will scrape articles from websites defined in the sites.yaml file.
 
 ```lemmatize``` will lemmatize all articles downloaded using ```scrape```.
 
 ```index``` will create a .json file for every downloaded article, which will contain key/value pairs of word/noOfOccurrences.
 
## Run server
In order to run the server, you have to run the following command:

```php -S localhost:8080 -t <path-to-projects-/web/www-folder>```

Afterwards, by going to ```localhost:8000```, you should see the project's homepage
  
# More websites
The scraper takes sites from ```sites.yaml``` where similar blogs are in comment block.
If you want to scrape more blogs, add them with the same structure with page list bounds and with the
target css class as well. ```scraper.py``` script would also need to be edited a bit.
