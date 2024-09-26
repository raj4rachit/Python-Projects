import scrapy
from myscraper.items import MyscraperItem

class ClutchSpider(scrapy.Spider):
    name = "clutch"
    allowed_domains = ["clutch.co"]
    start_urls = ["https://clutch.co/it-services/new-york-state"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'})

    def parse(self, response):
        for quote in response.css('li.provider-row'):
            clutchdata = quote.css('div.row')
            item = MyscraperItem()
            item['name'] = clutchdata.css('div.provider-info--header h3.company_info a.company_title::text').get()
            yield item

        # Following the pagination link
        next_page = response.css('li.next > a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'})
