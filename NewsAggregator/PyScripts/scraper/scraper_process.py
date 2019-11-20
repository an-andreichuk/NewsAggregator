#!/usr/bin/env python
import scrapy
from scrapy.crawler import CrawlerProcess
import time
from twisted.internet import reactor
from twisted.internet.task import deferLater
import pymongo
from pymongo import MongoClient
import datetime
from datetime import timedelta, datetime, tzinfo, timezone
from scrapy.utils.project import get_project_settings

news_urls = []
checked_news = []
domain = "https://www.pravda.com.ua"

client = MongoClient('mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority')
db = client['News']
collection = db['pravda.com.ua']

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        self.urls = [
            'https://www.pravda.com.ua'
        ]
        
        for url in news_urls + self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        if response.request.url in checked_news:
            return
        
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

            for x in response.xpath('//div[@class="post_news__text"]/p//text()').extract():
                Text.replace('\n','')
                Text += x
                Text += '\n'
            
            for x in response.xpath('//span[@class="post__tags__item"]/a/text()').extract():
            	Tags.append(x)
            
            collection.insert_one({'Title': Title,
                'Text': Text,
                'SourceUrl': SourceUrl,
                'TimeSourcePublished': TimeSourcePublished,
                'Tags':Tags})
        
        checked_news.append(response.request.url)


process = CrawlerProcess(get_project_settings())
counter = 0

def _crawl(result, spider):
    global counter

    if counter > 1:
        time.sleep(888)

    counter+= 1
    deferred = process.crawl(spider)
    deferred.addCallback(_crawl, spider)
    return deferred

_crawl(None,QuotesSpider)
process.start() 