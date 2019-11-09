using MongoDB.Driver;
using System.Collections.Generic;

namespace NewsAggregator.Models
{
    public class MongoDbContext
    {
        private readonly IMongoDatabase _mongoDb;
        private List<IMongoCollection<NewsEntry>> _currNews;

        public MongoDbContext()
        {
            var client = new MongoClient("mongodb+srv://an-andreichuk:pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority");
            _mongoDb = client.GetDatabase("News");
            _currNews = new List<IMongoCollection<NewsEntry>>();
        }
        public List<IMongoCollection<NewsEntry>> News
        {
            get
            {
                _currNews.Clear();

                _currNews.Add(_mongoDb.GetCollection<NewsEntry>("pravda.com.ua"));
                _currNews.Add(_mongoDb.GetCollection<NewsEntry>("tsn.ua"));
                
                return _currNews;
            }
        }
    }
}
