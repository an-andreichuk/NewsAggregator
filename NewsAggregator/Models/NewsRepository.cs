using MongoDB.Driver;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace NewsAggregator.Models
{
    public class NewsRepository : INewsRepository
    {
        MongoDbContext db = new MongoDbContext();
        public async Task<IEnumerable<NewsEntry>> GetAllNews()
        {
            try
            {
                var allNews = db.News;

                //some smart logic here e.g. news comparation
                //actually the result of some smart function should be here
                var selectedNews = MergeNews(allNews);
                
                var sortedNews = selectedNews.Find(_ => true).
                                  SortByDescending(news => news.TimeSourcePublished);
                return await sortedNews.ToListAsync();
            }
            catch
            {
                throw;
            }
        }

        private IMongoCollection<NewsEntry> MergeNews(List<IMongoCollection<NewsEntry>> allNews)
        {
            var res = allNews.First();
            foreach(var news in allNews)
            {
                if (news.Equals(allNews.First()))
                    continue;

                res.InsertManyAsync(news.AsQueryable());
            }
            return res;
        }
    }
}
