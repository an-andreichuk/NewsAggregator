﻿using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;
using System.Collections;
using Newtonsoft.Json;
using NewsAggregator.Utils;

namespace NewsAggregator.Models
{
    public static class NewsHelper
    {
        public static async Task<List<NewsEntry>> AnalyseNewsAsync(List<IMongoCollection<NewsEntry>> allNews)
        {
            //some smart logic here e.g. news comparation
            //actually, the result of some smart function should be the output of this func


            var selectedNews = await MergeNewsAsync(allNews);

            //need to add news translation for beter analysis
            //actually, if you want this to work, you need to add locally a private key as project environment variable named GOOGLE_APPLICATION_CREDENTIALS
            //you can ask me for this private key
            var translatedNews = TranslateNews(selectedNews);

            return translatedNews;
        }

        public static async Task<IEnumerable<NewsEntry>> 
            GetRecentNews(List<IMongoCollection<NewsEntry>> allNews)
        {
            var selectedNews = await MergeNewsAsync(allNews);
            
            var sortedNews = selectedNews.
                OrderByDescending(news => news.TimeSourcePublished);
            
            return sortedNews;
        }

        public static List<NewsEntry> TranslateNews(List<NewsEntry> news)
        {
            //need to add smarter logic here...

            var translatedNews = news;
            int count = 0;

            foreach (var newsEntry in translatedNews)
            {
                if (string.IsNullOrEmpty(newsEntry.EnglishText))
                {
                    newsEntry.EnglishText = new GoogleTranslator().TranslateText(newsEntry.Text, "en");
                    ++count;
                }

                if (count > 0)  //translates only 1 news per attempt - Rate Limit issue
                    break;
            }

            return translatedNews;
        }

        public static async Task<List<NewsEntry>> MergeNewsAsync(List<IMongoCollection<NewsEntry>> allNews)
        {
            var res = new List<NewsEntry>();

            foreach (var newsCollection in allNews)
            {
                res.InsertRange(res.Count,
                    await newsCollection.Find(_ => true).ToListAsync());
            }

            return res;
        }
    }
}