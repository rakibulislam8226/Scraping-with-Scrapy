import scrapy


class QuotesSpiderItem(scrapy.Item):
    """define the fields for quotes item here"""

    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
