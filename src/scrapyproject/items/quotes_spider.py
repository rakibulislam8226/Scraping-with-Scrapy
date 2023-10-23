import scrapy


class QuotesSpiderItem(scrapy.Item):
    """define the fields for quotes item here"""

    Text = scrapy.Field()
    Author = scrapy.Field()
    Tags = scrapy.Field()
