import pymongo
from bs4 import BeautifulSoup
import requests
import urllib.request
import numpy as np


myclient = pymongo.MongoClient("mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["news"]
mycol = mydb["24tv.ua"]

surl = "https://24tv.ua/" #short url
url = "https://24tv.ua/novini_tag1117/"

r1 = requests.get(url)

coverpage = r1.content
soup1 = BeautifulSoup(coverpage, 'html5lib')
coverpage_news = soup1.find_all('a', class_="news_title")



# Scraping articles we got
number_of_articles = len(coverpage_news)

# Empty lists for content, links and titles

news_contents = ''
list_links = []
list_titles = []

for n in np.arange(0, number_of_articles):

    # Getting the link of the article
    link = coverpage_news[n]['href']
    link = surl + link
    print(link)
    list_links.append(link)
    SourceUrl = link

    # Getting the title
    Title = coverpage_news[n].get_text()
    list_titles.append(Title)

    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content, 'html5lib')
    body = soup_article.find_all('div', class_="article_text")
    x = body[0].find_all('p')

    # Getting he tags
    tag_list = soup_article.find_all('div', class_="tags")
    t = tag_list[1].find_all('a')
    Tags = []
    for i in np.arange(0, len(t)):
        Tags.append(t[i].get_text())

    # Getting time & date
    TimeSourcePublished = soup_article.time["datetime"]

    list_paragraphs = ''
    final_article = ''
 
 
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        
        list_paragraphs += paragraph
        
        final_article += list_paragraphs


    
    news_contents += final_article
    Text = news_contents
    

    EnglishText = ''
    KeyWords = ''
    Duplicates = ''

    result = {
    "Title": Title,
    "Text": Text,
    "Tags": Tags,
    "SourceUrl": SourceUrl,
    "TimeSourcePublished": TimeSourcePublished,
    "EnglishText": EnglishText,
    "KeyWords": KeyWords,
    "Duplicates": Duplicates
    }

    mycol.insert_one(result)


