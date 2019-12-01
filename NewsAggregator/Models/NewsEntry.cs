using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.Collections.Generic;

namespace NewsAggregator.Models
{
    public class NewsEntry
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; private set; }
        public string Title { get; private set; }
        public string Text { get; private set; }
        public List<string> Tags { get; set; }
        public string SourceUrl { get; private set; }
        public BsonDateTime TimeSourcePublished { get; private set; }
        public string EnglishText { get; set; }
        public List<string> KeyWords { get; set; }
        public List<string> DuplicateUrls { get; set; }
        public string Sentiment {get; set; } 
    }
}