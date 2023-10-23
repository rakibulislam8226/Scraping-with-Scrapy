import scrapy

from ..items.quotes_spider import QuotesSpiderItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        URL = "https://quotes.toscrape.com/"
        yield scrapy.Request(url=URL, callback=self.response_parser)

    def response_parser(self, response):
        items = QuotesSpiderItem()

        for selector in response.css(".quote"):
            text = (selector.css("span.text::text").extract_first(),)
            author = (selector.css(".author::text").extract_first(),)
            tags = (selector.css(".tag::text").extract(),)

            items["Text"] = text
            items["Author"] = author
            items["Tags"] = tags

            yield items

        next_page_link = response.css("li.next a::attr(href)").extract_first()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.response_parser)
