import scrapy
from scrapy_splash import SplashRequest


class QuotesJsSpider(scrapy.Spider):
    name = 'quotes_js_spider'
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'quote': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SplashRequest(next_page, callback=self.parse)
