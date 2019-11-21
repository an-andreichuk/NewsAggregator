#!/usr/bin/env python
import re
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
domain = "https://www.pravda.com.ua"

client = MongoClient(
    'mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority')
db = client['News']
collection = db['pravda.com.ua']


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        self.urls = [
            'https://www.pravda.com.ua'
        ]
        not_scraped = list(set(news_urls) - set(checked_news))
        for url in not_scraped + self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.request.url in self.urls:
            for x in response.xpath('//div[@class="article__title"]//a/@href').extract():
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

            if len(response.xpath('//h1[@class="post_news__title"]').extract()) != 0:
                Title = response.xpath('//h1[@class="post_news__title"]//text()').extract()[0]
            else:
                return
            text_parts = response.xpath('//div[@class="post_news__text"]/p//text()').extract()
            normalized_article_strings = utils.normalize(text_parts)
            Text = "\n".join(normalized_article_strings)
            for x in response.xpath('//span[@class="post__tags__item"]/a/text()').extract():
                Tags.append(x)

            collection.insert_one({'Title': Title,
                                   'Text': Text,
                                   'SourceUrl': SourceUrl,
                                   'TimeSourcePublished': TimeSourcePublished,
                                   'Tags': Tags})

            checked_news.append(response.request.url)


process = CrawlerProcess(get_project_settings())
counter = 0
checked_news = utils.get_checked_news(collection)

print(checked_news)

def _crawl(result, spider):
    global counter

    if counter > 1:
        time.sleep(888)

    counter += 1
    deferred = process.crawl(spider)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, QuotesSpider)
process.start()
