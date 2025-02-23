import scrapy

class NewsScraperItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
