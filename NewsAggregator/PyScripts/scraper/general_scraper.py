#!/usr/bin/env python
import scrapy
import time
import pymongo
import datetime
import utils
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from twisted.internet.task import deferLater
from pymongo import MongoClient
from datetime import timedelta, datetime, tzinfo
from scrapy.utils.project import get_project_settings

news_urls = []
checked_news = []

client = MongoClient(
    'mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority')
db = client['News']
collection_platforma = db['platfor.ma']
collection_gordon = db['gordon.ua']
collection_pravda = db['pravda.com.ua']
parameters = {
    "platforma": {
        "name": "platforma",
        "collection": collection_platforma,
        "domain": "https://platfor.ma/topics/knowledge/",
        "start_urls_list": ['https://platfor.ma/topics/knowledge/'],
        "xpath_for_collecting_links": """
            //div[@id='wrap-to-posts']/div[@class='article']/a[@class='full-link']/@href""",
        # xpath_for_title should always be provided without '//text()'
        "xpath_for_title": """
            //body[contains(@class, 'theme-template-default single single-theme postid-')]
            /section[contains(@class, 'type-')]/h2[@class='article-name']/span""",
        "xpath_for_article": """
            //div[@class='wrapper large row mob-flex-wrap']/div[contains(@class, 'column type-')]
            /article/div[contains(@class, 'block type-') and not (contains(@class, 'block type-21')) 
            and not (contains(@class, 'block type-16'))]//text()""",
        "xpath_for_tags": "//div[@class='tags']//text()"
    },
    "gordon": {
        "name": "gordon",
        "collection": collection_gordon,
        "domain": "https://gordonua.com/ukr/",
        "start_urls_list": ['https://gordonua.com/ukr/'],
        "xpath_for_collecting_links": '//div[@class="tab-content"]//a/@href',
        # xpath_for_title should always be provided without '//text()'
        "xpath_for_title": '//h1[@class="a_head flipboard-title"]',
        "xpath_for_article": '//div[@class="a_body"]/p/text()',
        "xpath_for_tags": '//div[@class="tags flipboard-endArticle"]/a/text()'
    },
    "pravda": {
        "name": "quotes",
        "collection": collection_pravda,
        "domain": "https://www.pravda.com.ua",
        "start_urls_list": ["https://www.pravda.com.ua"],
        "xpath_for_collecting_links": '//div[@class="article__title"]//a/@href',
        # xpath_for_title should always be provided without '//text()'
        "xpath_for_title": '//h1[@class="post_news__title"]',
        "xpath_for_article": '//div[@class="post_news__text"]/p//text()',
        "xpath_for_tags": '//span[@class="post__tags__item"]/a/text()'
    }
}


class GeneralSpider(scrapy.Spider):
    def __init__(self, **kwargs):
        super(GeneralSpider, self).__init__(**kwargs)
        self.params = kwargs.get("spider_params")
    name = "general_spider"

    def start_requests(self):
        self.urls = self.params["start_urls_list"]
        not_scraped = list(set(news_urls) - set(checked_news))
        for url in not_scraped + self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        domain = self.params["domain"]
        if response.request.url in self.urls:
            for x in response.xpath(self.params["xpath_for_collecting_links"]).extract():
                if len(x) > 0 and x[0] == '/':
                    x = domain + x
                if x.startswith(domain):
                    news_urls.append(x)
        else:
            Text = ""
            Title = ""
            SourceUrl = response.request.url
            Tags = []
            TimeSourcePublished = datetime.utcnow() + timedelta(hours=2)
            title_xpath = self.params["xpath_for_title"]
            if len(response.xpath(title_xpath).extract()) != 0:
                Title = response.xpath("{0}{1}".format(title_xpath, '//text()')).extract()[0]
            else:
                return
            texts_parts_xpath = self.params["xpath_for_article"]
            text_parts = response.xpath(texts_parts_xpath).extract()
            normalized_article_strings = utils.normalize(text_parts)
            Text = "\n".join(normalized_article_strings)
            tags_response = response.xpath(self.params["xpath_for_tags"]).extract()
            for x in utils.normalize(tags_response):
                Tags.append(x)

            self.params["collection"].insert_one({'Title': Title,
                                                  'Text': Text,
                                                  'SourceUrl': SourceUrl,
                                                  'TimeSourcePublished': TimeSourcePublished,
                                                  'Tags': Tags})

            checked_news.append(response.request.url)


process = CrawlerProcess(get_project_settings())
counter = 0

print(checked_news)


def _crawl(result, spider, collection, params):
    global counter

    if counter > 1:
        time.sleep(888)

    counter += 1
    checked_news = utils.get_checked_news(collection)
    deferred = process.crawl(spider, spider_params=params)
    deferred.addCallback(_crawl, spider, params)
    return deferred


_crawl(None, GeneralSpider, collection=collection_pravda, params=parameters["pravda"])
# _crawl(None, GeneralSpider, collection=collection_gordon, params=parameters["gordon"])
# _crawl(None, GeneralSpider, collection=collection_platforma, params=parameters["platforma"])
process.start()
