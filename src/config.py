from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_CSV = PROJECT_ROOT / "data" / "processed" / "books_scraped.csv"
DB = PROJECT_ROOT / "data" / "database.db"
LOG = PROJECT_ROOT / "logs" / "log.txt"
HIST = PROJECT_ROOT / "docs" / "histogram.png"
BAR_CHART = PROJECT_ROOT / "docs" / "bar_chart.png"
PIE_CHART = PROJECT_ROOT / "docs" / "pie_chart.png"
WEBSITE = "https://books.toscrape.com/catalogue/page-{page}.html"
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
NEWS_WEBSITE = "https://news.ycombinator.com/?p={page}"
SOURCE_NAME = "Hacker News"
COMPANIES = ["Apple", "Google", "Microsoft", "OpenAI", "Anthropic"]
