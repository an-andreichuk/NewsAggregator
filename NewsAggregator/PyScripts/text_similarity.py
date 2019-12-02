# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 12:45:06 2019

@author: Gannusya
"""
"""
pip install googletrans
conda install pymongo[srv]
pip install vaderSentiment
pip install bert-extractive-summarizer
"""
from pymongo import MongoClient

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import string
import requests
import pandas as pd
from semantic_text_similarity.models import WebBertSimilarity
def sentiment_analyzer_scores(text):
    score = analyzer.polarity_scores(text)
    print(score)
#client = MongoClient("mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority")
#db = client["News"]

#mycol = db["pravda.com.ua"]
dd = {}
web_model = WebBertSimilarity(device='cpu', batch_size=10) #defaults to GPU prediction
print(web_model.predict([("She won an olympic gold medal","The women is an olympic champion")]))
print(web_model.predict([("You are a loser","You are a champion")]))
"""
for document in mycol.find():
    try:
        analyzer = SentimentIntensityAnalyzer()
        dic = analyzer.polarity_scores(document["EnglishText"]);
        document["Sentiment"] = dic['pos']
        dd[document["SourceUrl"]] = dd['Text']
    except:
        print("ERROR")
"""
x = mycol.find_one()

#
#model(x['EnglishText'])
#print(x)
print(db.list_collection_names())
