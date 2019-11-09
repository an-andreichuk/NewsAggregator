using System.Collections.Generic;
using System.Threading.Tasks;

namespace NewsAggregator.Models
{
    public interface INewsRepository
    {
        Task<IEnumerable<NewsEntry>> GetAllNews();
        Task<NewsEntry> GetNewsEntry(string id);
    }
}
