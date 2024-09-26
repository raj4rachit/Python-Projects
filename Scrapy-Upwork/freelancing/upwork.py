from scrapy.spiders import CrawlSpider, Rule 
from scrapy.linkextractors import LinkExtractor


class UpworkSpider(CrawlSpider):
    name = 'upwork_spider'
    start_urls = [
        'https://www.upwork.com/freelance-jobs/'
    ]
    allowed_domains = [
        'upwork.com'
    ]
    rules = [
        Rule(link_extractor=LinkExtractor(
            allow='/freelance-jobs/\w+',
            canonicalize=True,
        ), 
        follow=True,
        callback='parse_category',
        )
    ]

    def parse(self, response):
        self.logger.info(f'[parse] Response from {response.url} has arrived.')
    
    def parse_category(self, response):
        self.logger.info(f'[parse_category] Response from {response.url} has arrived.')

    def parse_item(self, item):
        pass

    def parse_item_details(self, item):
        pass
