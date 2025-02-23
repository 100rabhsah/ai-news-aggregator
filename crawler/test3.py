import sqlite3
import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess

# Database setup
DB_PATH = "news.db"

def initialize_db():
    """Ensure the news table has the correct schema, including sub_category."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            link TEXT UNIQUE,
            content TEXT,
            category TEXT,
            sub_category TEXT
        )
    """)
    try:
        cursor.execute("ALTER TABLE news ADD COLUMN sub_category TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  

    conn.close()

def fetch_article_content(url):
    """Fetch full article content from a news article URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/133.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "Content not available."

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract article text
        paragraphs = soup.find_all("p")
        if paragraphs:
            return " ".join([p.get_text(strip=True) for p in paragraphs])[:500]  # Limit content size

        return "Content extraction failed."
    except Exception as e:
        return f"Error fetching content: {str(e)}"

def classify_news(title):
    """Classify news into Global/Local and assign a sub-category."""
    global_topics = ["World", "Politics", "Business", "Technology", "Science", "Sports"]
    local_topics = ["India", "Uttar Pradesh", "Lucknow", "Delhi", "Mumbai", "Bengaluru"]

    category = "Global"
    sub_category = "General"

    for topic in global_topics:
        if topic.lower() in title.lower():
            category = "Global"
            sub_category = topic
            break
    
    for topic in local_topics:
        if topic.lower() in title.lower():
            category = "Local"
            sub_category = topic
            break

    return category, sub_category

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["www.bing.com"]
    start_urls = ["https://www.bing.com/news/search?q=latest+news"]

    def parse(self, response):
        """Extracts news headlines and links from Bing search results."""
        for article in response.css("div.news-card"):
            title = article.css("a.title::text").get()
            link = article.css("a.title::attr(href)").get()

            if title and link:
                category, sub_category = classify_news(title)
                content = fetch_article_content(link)

                # Store in SQLite database
                store_news(title, link, category, sub_category, content)

                print(f"✅ {title}")
                print(f"🔗 {link}")
                print(f"🏷️ {category} → {sub_category}")
                print("-" * 50)

def store_news(title, link, category, sub_category, content):
    """Store news in SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO news (source, title, link, content, category, sub_category)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Bing News", title, link, content, category, sub_category))

    conn.commit()
    conn.close()

def run_scraper():
    """Runs Scrapy spider to fetch news dynamically."""
    initialize_db()
    
    process = CrawlerProcess({
        "LOG_LEVEL": "ERROR",  # Hide unnecessary logs
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/133.0.0.0 Safari/537.36"
    })
    process.crawl(NewsSpider)
    process.start()
    print("✅ News scraping completed!")

if __name__ == "__main__":
    run_scraper()
