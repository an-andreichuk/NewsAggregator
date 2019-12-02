using Microsoft.AspNetCore.Mvc;
using MongoDB.Bson;
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
                await UpdateNews();
                return await NewsHelper.GetRecentNews(db.News);
            }
            catch
            {
                throw;
            }
        }

        public async Task UpdateNews()
        {
            try
            {
                var updatedNews = await NewsHelper.AnalyseNewsAsync(db.News);

                foreach(var newsEntry in updatedNews)
                {
                    for (int idx = 0; idx < db.News.Count; ++idx)
                    {
                        await db.News[idx].ReplaceOneAsync(
                            n => n.Id == newsEntry.Id, newsEntry);
                    }
                }
            }
            catch
            {
                throw;
            }
        }

        public Task<ActionResult> Create(NewsEntry entry)
        {
            throw new NotImplementedException();
        }

        public Task<ActionResult> Update(string id, NewsEntry entry)
        {
            throw new NotImplementedException();
        }
    }
}
