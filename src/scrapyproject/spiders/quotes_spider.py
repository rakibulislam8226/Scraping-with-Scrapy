import scrapy

from ..items.quotes_spider import QuotesSpiderItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # NOTE: custom setting for pipelines but now am use default setting in setting.py
    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "scrapyproject.pipelines.QuotesPipelineWithSqlite": 300,  # Pipelines for quotes spider with Sqlite3
    #     }
    # }

    def start_requests(self):
        URL = "https://quotes.toscrape.com/"
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        items = QuotesSpiderItem()

        for selector in response.css(".quote"):
            text = (selector.css("span.text::text").extract_first(),)
            author = (selector.css(".author::text").extract_first(),)
            tags = (selector.css(".tag::text").extract(),)

            items["text"] = text
            items["author"] = author
            items["tags"] = tags

            yield items

        next_page_link = response.css("li.next a::attr(href)").extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)
