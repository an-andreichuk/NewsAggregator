# -*- coding: utf8 -*-
from pymongo import MongoClient
import datetime
import pprint as pp
from analysis import NewsAnalyser


class MongoBD:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority')
        self.db = self.client['News']
        self.collection_names = self.db.list_collection_names()
        self.collections = [self.db[name] for name in self.collection_names]
        # just phony news
        self.recent_news_cursors = [col.find({"TimeSourcePublished": {"$gte": datetime.datetime(2019, 11, 21, 0), "$lte": datetime.datetime(2019, 11, 24, 23)}}) for col in self.collections]
        self.analyser = NewsAnalyser()

    def setRecentNewsCursors(self):
        today = datetime.date.today()
        self.recent_news_cursors = [col.find({"TimeSourcePublished": {"$gte": datetime.datetime(today.year, today.month, today.day, 0, 0, 0), "$lte": datetime.datetime(today.year, today.month, today.day, 23, 59, 59)}}) for col in self.collections]

    def getRecentNewsFromCursor(self, cursor):
        news = []
        for item in cursor:
            news.append(item)
        return news

    def updateNews(self):
        count = 0
        for cursor in self.recent_news_cursors:
            news = self.getRecentNewsFromCursor(cursor)
            news = self.analyser.translateTextToEnglish(news)
            news = self.analyser.sentimentAnalysis(news)
            news = self.analyser.autoTag(news)
            news = self.analyser.summary(news)
            news = self.analyser.translateSummaryToUkr(news)
            for entry in news:
                cursor.collection.update({"_id": entry["_id"]}, {"$set": entry})
                count += 1

        print("Updated {} news.".format(count))


if __name__ == "__main__":
    db = MongoBD()
    db.setRecentNewsCursors()
    db.updateNews()
