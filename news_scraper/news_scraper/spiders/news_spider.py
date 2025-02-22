import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class NewsSpider(CrawlSpider):
    name = "news_spider"
    
    def __init__(self, topic=None, sub_topics=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.sub_topics = sub_topics.split(",") if sub_topics else []
        
        # Define the start URLs dynamically
        self.start_urls = [
            "https://www.bbc.com/sport/cricket"  # General cricket news page
        ]
    
    # Define rules for following links
    rules = (
        Rule(LinkExtractor(allow=r"/sport/cricket/\d+"), callback="parse_item"),  # Follow links to articles
    )
    
    def parse_item(self, response):
        # Extract article details
        title = response.css("h1::text").get()  # Assuming the title is in <h1>
        content = " ".join(response.css("p::text").getall())  # Assuming content is in <p>
        
        # Extract the sub-topic from the URL or content
        sub_topic = None
        for st in self.sub_topics:
            if st.lower() in content.lower():
                sub_topic = st
                break
        
        # Yield the extracted data
        if sub_topic:  # Only yield articles that match the sub-topics
            yield {
                "topic": self.topic,
                "sub_topic": sub_topic,
                "title": title,
                "content": content,
                "url": response.url,
            }