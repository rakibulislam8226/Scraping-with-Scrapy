import scrapy

from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

from ..items.quotes_spider import QuotesSpiderItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        URL = "https://quotes.toscrape.com/login"
        yield FormRequest(
            URL,
            formdata={"username": "example@gmail.com", "password": "rakib123"},
            callback=self.response_parser,
        )

    def response_parser(self, response):
        # open_in_browser(response)
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
