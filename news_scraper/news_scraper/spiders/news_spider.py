import scrapy
import json
from newspaper import Article
from news_scraper.items import NewsScraperItem
from transformers import pipeline

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["timesofindia.indiatimes.com", "ndtv.com", "thehindu.com", "espn.com"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'temp_news.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    start_urls = [
        "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "https://feeds.feedburner.com/ndtvnews-top-stories",
        "https://www.thehindu.com/news/national/feeder/default.rss",
        "https://www.espn.com/espn/rss/news"
    ]

    MAX_TOTAL_ARTICLES = 50  # Keep the limit as requested

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summarizer = pipeline("summarization", model="t5-small")
        self.total_articles = 0  # Track total articles scraped

    def parse(self, response):
        """Extract article links from RSS feeds."""
        self.logger.info(f"Parsing RSS Feed: {response.url}")

        for item in response.xpath("//item"):
            if self.total_articles >= self.MAX_TOTAL_ARTICLES:
                break  # Stop scraping if the limit is reached

            title = item.xpath("title/text()").get()
            link = item.xpath("link/text()").get()
            description = item.xpath("description/text()").get(default="")

            if title and link:
                if len(description) > 100:
                    summary = self.summarize_text(description)
                    category, sub_category = self.classify_news(title)

                    yield NewsScraperItem(
                        source=response.url,
                        title=title,
                        link=link,
                        content=summary,
                        category=category,
                        sub_category=sub_category
                    )
                else:
                    yield scrapy.Request(url=link, callback=self.parse_article, meta={"title": title, "source": response.url})

    def parse_article(self, response):
        """Extract full content and enforce article limit."""
        if self.total_articles >= self.MAX_TOTAL_ARTICLES:
            return  # Stop if limit reached

        paragraphs = response.xpath("//p//text()").getall()
        content = " ".join(paragraphs).strip()

        if len(content) < 100:
            article = Article(response.url)
            article.download()
            article.parse()
            content = article.text if article.text else "Content extraction failed."

        self.total_articles += 1  # Increase count

        category, sub_category = self.classify_news(response.meta["title"])

        yield NewsScraperItem(
            source=response.meta["source"],
            title=response.meta["title"],
            link=response.url,
            content=self.summarize_text(content),
            category=category,
            sub_category=sub_category
        )

    def summarize_text(self, text):
        """Summarize text if too long."""
        if len(text) > 1000:
            return self.summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
        return text

    def classify_news(self, title):
        """Classify news into Global/Local categories."""
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
