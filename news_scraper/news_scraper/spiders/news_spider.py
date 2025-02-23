import scrapy
import json
from newspaper import Article
from news_scraper.items import NewsScraperItem

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["timesofindia.indiatimes.com", "ndtv.com", "thehindu.com", "espn.com"]
    
    start_urls = [
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://feeds.feedburner.com/ndtvnews-top-stories",
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://www.espn.com/espn/rss/news"
    ]

    def parse(self, response):
        """Extract article links from RSS feeds."""
        self.logger.info(f"Parsing RSS Feed: {response.url}")
        
        for item in response.xpath("//item"):
            title = item.xpath("title/text()").get()
            link = item.xpath("link/text()").get()

            if title and link:
                yield scrapy.Request(url=link, callback=self.parse_article, meta={"title": title, "source": response.url})

    def parse_article(self, response):
        """Extract full content using newspaper3k and Scrapy."""
        article = Article(response.url)
        article.download()
        article.parse()
        
        content = article.text[:500] if article.text else "Content extraction failed."
        category, sub_category = self.classify_news(response.meta["title"])
        
        yield NewsScraperItem(
            source=response.meta["source"],
            title=response.meta["title"],
            link=response.url,
            content=content,
            category=category,
            sub_category=sub_category
        )

    def classify_news(self, title):
        """Classify news into global/local categories."""
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
