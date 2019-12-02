using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace NewsAggregator.Models
{
    public interface INewsRepository
    {
        Task<IEnumerable<NewsEntry>> GetAllNews();
        Task<NewsEntry> GetNewsEntry(string id);
        Task<ActionResult> Create(NewsEntry entry);
        Task<ActionResult> Update(string id, NewsEntry entry);
    }
}
