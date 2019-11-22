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

        public async Task<NewsEntry> GetNewsEntry(string id)
        {
            try
            {
                FilterDefinition<NewsEntry> filter = Builders<NewsEntry>.Filter.Eq("Id", id);
                foreach (var news in db.News)
                {
                    var entry = news.Find(filter);
                    if (entry.Any())
                        return await entry.FirstOrDefaultAsync();
                }
                throw new Exception("Invalid id");
            }
            catch
            {
                throw;
            }
        }

        public async Task<IEnumerable<NewsEntry>> GetAllNews()
        {
            try
            {
                return await NewsHelper.GetRecentNews(db.News);
            }
            catch
            {
                throw;
            }
        }
    }
}
