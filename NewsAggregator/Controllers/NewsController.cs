using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using System.Net;  
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using NewsAggregator.Models;
using Microsoft.AspNetCore.Http;

namespace NewsAggregator.Controllers
{
    public class NewsController : Controller
    {
        
        private readonly INewsRepository _dataAccessProvider = new NewsRepository();
        public async Task<ActionResult> Index()
        {
            IEnumerable<NewsEntry> allNews = await _dataAccessProvider.GetAllNews();
            return View(allNews);
        }

        public async Task<ActionResult> Details(string id)
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

        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

    }
}
