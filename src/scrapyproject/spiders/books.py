import scrapy

from ..items.books import BooksSpiderItem


class BooksSpider(scrapy.Spider):
    name = "books"
    # NOTE: custom setting for pipelines but now am use default setting in setting.py
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "scrapyproject.pipelines.BooksPipelineWithMySQL": 300,  # Pipelines for books spider with MySQL database
    #     }
    # }

    def start_requests(self):
        URL = "https://books.toscrape.com/"
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        items = BooksSpiderItem()

        for selector in response.css("article.product_pod"):
            items["image"] = (selector.css("a > img::attr(src)").extract_first(),)
            items["image_alt"] = (selector.css("a > img::attr(alt)").extract_first(),)
            items["title"] = (selector.css("h3 > a::attr(title)").extract_first(),)
            items["price"] = (selector.css(".price_color::text").extract_first(),)
            items["stock"] = (selector.css(".availability::text").extract(),)

        yield items

        next_page_link = response.css("li.next a::attr(href)").extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)
