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
domain = "https://platfor.ma/topics/knowledge/"

client = MongoClient(
    'mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority')
db = client['News']
collection = db['pravda.com.ua']


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        self.urls = [
            'https://platfor.ma/topics/knowledge/'
        ]
        not_scraped = list(set(news_urls) - set(checked_news))
        for url in not_scraped + self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.request.url in self.urls:
            for x in response.xpath("""
            //div[@id='wrap-to-posts']/div[@class='article']/a[@class='full-link']/@href""").extract():
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
            title_xpath = """
            //body[contains(@class, 'theme-template-default single single-theme postid-')]
            /section[contains(@class, 'type-')]/h2[@class='article-name']/span"""
            if len(response.xpath(title_xpath).extract()) != 0:
                Title = response.xpath("{0}{1}".format(title_xpath, '//text()')).extract()[0]
            else:
                return
            texts_parts_xpath = """
            //div[@class='wrapper large row mob-flex-wrap']/div[contains(@class, 'column type-')]
            /article/div[contains(@class, 'block type-') and not (contains(@class, 'block type-21')) 
            and not (contains(@class, 'block type-16'))]//text()"""
            text_parts = response.xpath(texts_parts_xpath).extract()
            normalized_article_strings = utils.normalize(text_parts)
            Text = "\n".join(normalized_article_strings)
            tags_response = response.xpath("//div[@class='tags']//text()").extract()
            for x in utils.normalize(tags_response):
                Tags.append(x)

            collection.insert_one({'Title': Title,
                                   'Text': Text,
                                   'SourceUrl': SourceUrl,
                                   'TimeSourcePublished': TimeSourcePublished,
                                   'Tags': Tags})

            checked_news.append(response.request.url)


process = CrawlerProcess(get_project_settings())
counter = 0

print(checked_news)


def _crawl(result, spider):
    global counter

    if counter > 1:
        time.sleep(888)

    counter += 1
    checked_news = utils.get_checked_news(collection)
    deferred = process.crawl(spider)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, QuotesSpider)
process.start()
