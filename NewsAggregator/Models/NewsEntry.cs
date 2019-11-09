using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace NewsAggregator.Models
{
    public class NewsEntry
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; private set; }
        public string Title { get; private set; }
        public string Text { get; private set; }
        public string SourceUrl { get; private set; }
        public BsonDateTime TimeSourcePublished { get; private set; }
    }
}