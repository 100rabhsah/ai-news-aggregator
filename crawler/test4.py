import sqlite3
import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess
from duckduckgo_search import DDGS

# Database setup
DB_PATH = "newsagent.db"

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
    conn.commit()
    conn.close()

def fetch_article_content(url):
    """Fetch full article content from a news article URL with improved handling."""
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

        # Try different strategies to extract text
        article_text = []

        # 1. Try extracting from <article> tag
        article_tag = soup.find("article")
        if article_tag:
            article_text = article_tag.find_all("p")

        # 2. Fallback: Extract from all <p> tags
        if not article_text:
            article_text = soup.find_all("p")

        # 3. If <p> extraction fails, look for other common containers
        if not article_text:
            for tag in ["div", "section", "span"]:
                possible_text = soup.find_all(tag)
                if possible_text:
                    article_text = possible_text
                    break

        # Convert extracted text into a string (limit to 500 characters)
        if article_text:
            return " ".join([p.get_text(strip=True) for p in article_text])[:500]

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

class BingNewsSpider(scrapy.Spider):
    """Scrapes news from Bing News Search."""
    name = "bing_news"
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
                store_news("Bing News", title, link, category, sub_category, content)

                print(f"✅ {title}")
                print(f"🔗 {link}")
                print(f"🏷️ {category} → {sub_category}")
                print("-" * 50)

def fetch_duckduckgo_news():
    """Fetch news articles using DuckDuckGo search."""
    print("🔍 Fetching news from DuckDuckGo...")

    try:
        with DDGS() as ddgs:
            results = ddgs.news("latest news", max_results=10)  # Corrected method

        if results:
            for news in results:
                title = news.get("title")
                link = news.get("url")

                if title and link:
                    category, sub_category = classify_news(title)
                    content = fetch_article_content(link)

                    # Store in SQLite database
                    store_news("DuckDuckGo News", title, link, category, sub_category, content)

                    print(f"✅ {title}")
                    print(f"🔗 {link}")
                    print(f"🏷️ {category} → {sub_category}")
                    print("-" * 50)
        else:
            print("❌ No news found from DuckDuckGo.")

    except Exception as e:
        print(f"⚠️ Error fetching DuckDuckGo news: {e}")

def store_news(source, title, link, category, sub_category, content):
    """Store news in SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO news (source, title, link, content, category, sub_category)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (source, title, link, content, category, sub_category))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ Error storing news: {e}")

def run_scraper():
    """Runs Scrapy spider and DuckDuckGo news fetcher."""
    initialize_db()
    
    # Start Scrapy crawler for Bing News
    process = CrawlerProcess({
        "LOG_LEVEL": "ERROR",  # Hide unnecessary logs
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/133.0.0.0 Safari/537.36"
    })
    process.crawl(BingNewsSpider)
    process.start()
    
    # Fetch DuckDuckGo News
    fetch_duckduckgo_news()

    print("✅ News scraping completed!")

if __name__ == "__main__":
    run_scraper()
