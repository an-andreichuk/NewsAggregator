using MongoDB.Driver;
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
        public static async Task<IEnumerable<NewsEntry>> GetRecentNews(List<IMongoCollection<NewsEntry>> allNews)
        {
            //some smart logic here e.g. news comparation
            //actually the result of some smart function should be here
            var selectedNews = await MergeNewsAsync(allNews);

            var sortedNews = selectedNews.
                OrderByDescending(news => news.TimeSourcePublished);

            //need to add news translation for beter analysis
            //actually, you need to add locally a .json from the project root to environment variables for this to work
            var translatedText = new GoogleTranslator().TranslateText("якість новини", "en");
            
            return sortedNews;
        }

        public static async Task<List<NewsEntry>> MergeNewsAsync(List<IMongoCollection<NewsEntry>> allNews)
        {
            var res = new List<NewsEntry>();

            foreach (var news in allNews)
            {
                res.InsertRange(res.Count,
                    await news.Find(_ => true).ToListAsync());
            }

            return res;
        }
    }
}
