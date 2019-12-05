
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from threading import Thread
import time
import datetime

URL = 'https://www.bbc.com/news/world'

def get_article_urls(url = URL):
    '''
        returns article urls by given topic on bbc world
    '''

    response = requests.get(url)
    html_doc = bs(response.text, 'lxml')

    urls = []

    for a in html_doc.find_all('a', {'itemprop' : 'url'}):

        url = a.get('href')
        urls.append(url)

    return urls

def parse_article(url):
    '''
        Parse article page and returns dict in following format:

        {
            "_id": ObjectId,
            "Title": "string",
            "Text": "string",
            "Tags": [
                "string"
            ],
            "SourceUrl": "string",
            "TimeSourcePublished": BsonDate,
            "EnglishText": "string",,
            "KeyWords": [
                "string"
            ],
            "Duplicates": [
                "string"
            ]
        }
    '''

    try:
        response = requests.get(url)
        html_doc = bs(response.text, 'lxml')

        title = html_doc.find('h1', {'class' : 'ttl'}).text
        text = html_doc.find('div', {'class' : 'contentType'}).text

        tag_list = html_doc.find('ul', {'class':'teg-list'})
        tags = []

        if not tag_list is None:
            for tag in tag_list.find_all('li'):
                tags.append(tag.text)

        # example: 2019-12-04T15:12:00+02:00
        time = html_doc.find('meta', {'itemprop' : 'datePublished'}).get('content')
        time = datetime.datetime.fromisoformat(time)

        # there is no english source
        end_text = ""

        # highlighted words
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        keywords = article.keywords

        # field has no sense
        duplicates = []

        # mongo will create _id itself

        return {
            "Title" : title,
            "Text" : text,
            "Tags" : tags,
            "SourceUrl" : url,
            "TimeSourcePublished" : time,
            "EnglishText" : end_text,
            "KeyWords" : keywords,
            "Duplicates" : duplicates
        }

    except Exception as e:
        print('Error in "parse_article"',e)
        print('URL:', url)

class Parser(Thread):

    def __init__(self, mongo_client : MongoClient, db_name, table_name):
        super().__init__()
        self.finish = False
        self.mongo_client = mongo_client
        self.db_name = db_name
        self.table_name = table_name

    def finish_parsing(self):
        self.finish = True

    def run(self):

        lastUpdate = 0
        while not self.finish:

            results = []

            # if an hour have passed
            if time.time()-lastUpdate > 3600:

                for article in get_article_urls():
                    parse_result = parse_article(article)

                    if not parse_result == {}:
                        results.append(parse_result)

            else:
                time.sleep(60)
                continue

            self.mongo_client[self.db_name][self.table_name].insert_many(results)

            lastUpdate = time.time()
            print('News updated at:', datetime.datetime.fromtimestamp(lastUpdate).isoformat())
            print(len(results), 'results were added\n')


if __name__ == '__main__':
    mongo_client = MongoClient('localhost', 27017)

    p = Parser(mongo_client, 'db', 'bbc_parser')
    p.start()
