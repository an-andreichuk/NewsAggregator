﻿using MongoDB.Driver;
using System.Collections.Generic;

namespace NewsAggregator.Models
{
    public class MongoDbContext
    {
        private readonly IMongoDatabase _mongoDb;
        private List<IMongoCollection<NewsEntry>> _news;

        public MongoDbContext()
        {
            var client = new MongoClient("mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority");
            _mongoDb = client.GetDatabase("News");
            _news = new List<IMongoCollection<NewsEntry>>();
        }

        public List<IMongoCollection<NewsEntry>> News
        {
            get
            {
                _news.Clear();

                _news.Add(_mongoDb.GetCollection<NewsEntry>("pravda.com.ua"));
                _news.Add(_mongoDb.GetCollection<NewsEntry>("tsn.ua"));
                _news.Add(_mongoDb.GetCollection<NewsEntry>("unian.ua"));
                _news.Add(_mongoDb.GetCollection<NewsEntry>("hromadske.ua"));
                _news.Add(_mongoDb.GetCollection<NewsEntry>("bbc.com/ukrainian/news"));

                return _news;
            }
        }

        public List<string> CollectionNames
        {
            get
            {
                return _mongoDb.ListCollectionNamesAsync().Result.ToList();
            }
        }
    }
}
