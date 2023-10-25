import scrapy


class BooksSpiderItem(scrapy.Item):
    """define the fields for books item here"""

    image = scrapy.Field()
    image_alt = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
