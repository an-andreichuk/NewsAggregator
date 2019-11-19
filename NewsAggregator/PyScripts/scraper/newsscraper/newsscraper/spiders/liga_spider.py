import scrapy
import time

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        self.urls = [
            'https://news.liga.net/'
        ]
        self.news_urls = []
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
       pass
