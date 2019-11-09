using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using NewsAggregator.Models;

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

        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

    }
}
