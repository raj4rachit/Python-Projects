from scrapy.spiders import Spider 
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from scrapy import Request
from freelancing import items


class UpworkSpider(Spider):
    name = 'upwork_spider'
    start_urls = [
        'https://www.upwork.com/freelance-jobs/'
    ]
    allowed_domains = [
        'upwork.com'
    ]

    def parse(self, response):
        self.logger.info(f'[parse] Response from {response.url} has arrived.')
        job_item = items.JobCategory()
        job_categories = response.xpath("//ul[contains(@class, 'list-unstyled')]/ul")
        for cat in job_categories:
            try:
                print(cat)
                super_cat = cat.xpath("./h3/text()").extract()
                job_item['category_name'] = super_cat

                headings = list(map(lambda c: c.strip(), cat.xpath("./a/text()").getall()))

                urls = cat.xpath('./a/@href').extract()
                for i, url in enumerate(urls):
                    sub_job_item = items.JobCategory()
                    sub_job_item['category_name'] = headings[i]
                    yield Request(
                        response.urljoin(url), 
                        callback=self.parse_category_vacancies, 
                        cb_kwargs={'job_item': sub_job_item}
                    )
                    # parse only one sub category
                    break
            except IndexError:
                self.logger.info(f'Couldn\'t parse category \'{cat}\', continuing...')
            
            # parse only one supper category
            break

    def parse_category_vacancies(self, response, **cache):
        job_item = cache['job_item']
        cards = response.xpath("//section[@data-created-at]")
        vacancies = []
        for card in cards:
            vacancy = items.JobVacancy()
            vacancy['date_created'] = card.xpath("@data-created-at").get()
            vacancy['url'] = response.urljoin(card.xpath("./@data-url").get('not-found'))
            vacancy['name'] = response.xpath(".//h4/text()").get('').strip()
            payment_val = response.xpath(".//p/strong[contains(text(), '$')]/text()").get('').strip()
            vacancy['payment_type'] = 'Fixed price' if payment_val else ''
            vacancy['payment_value'] = payment_val
            vacancy['description'] = remove_tags(response.xpath(".//p[contains(@class, 'job-description')]").get(''))
            vacancy['tags'] = list(map(lambda x: x.strip(), response.xpath(".//div[contains(@class, 'skills-list')]/a/text()").getall()))
            
            vacancies.append(vacancy)

        job_item['vacancies'] = vacancies
        
        yield job_item
