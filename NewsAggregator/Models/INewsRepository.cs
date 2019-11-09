using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace NewsAggregator.Models
{
    public interface INewsRepository
    {
        Task<IEnumerable<NewsEntry>> GetAllNews();
    }
}
