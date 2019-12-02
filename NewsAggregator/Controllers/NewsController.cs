using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using NewsAggregator.Models;
using Microsoft.AspNetCore.Http;

namespace NewsAggregator.Controllers
{
    [Route("news/[controller]")]
    [ApiController]
    public class NewsController : Controller
    {
        private readonly INewsRepository _dataAccessProvider = new NewsRepository();

        [HttpGet]
        public async Task<ActionResult> Get()
        {
            IEnumerable<NewsEntry> allNews = await _dataAccessProvider.GetAllNews();
            return View(allNews);
        }

        [HttpGet("{id:length(24)}", Name = "GetNews")]
        public async Task<ActionResult> Get(string id)
        {
            if (id == null)
            {
                return new StatusCodeResult(400);
            }
            NewsEntry newsEntry = await _dataAccessProvider.GetNewsEntry(id);
            if (newsEntry == null)
            {
                return new StatusCodeResult(404);
            }
            return View(newsEntry);
        }

        [HttpPost]
        public async Task<ActionResult> Create(NewsEntry entry)
        {
            await _dataAccessProvider.Create(entry);

            return CreatedAtRoute("GetNews", new { id = entry.Id.ToString() }, entry);
        }

        [HttpPut("{id:length(24)}")]
        public async Task<ActionResult> Update(string id, NewsEntry newEntry)
        {
            if (id == null)
            {
                return new StatusCodeResult(400);
            }
            var oldEntry = await _dataAccessProvider.GetNewsEntry(id);

            if (oldEntry == null)
            {
                return new StatusCodeResult(404);
            }

            await _dataAccessProvider.Update(id, newEntry);

            return NoContent();
        }



        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

    }
}
