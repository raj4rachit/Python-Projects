import scrapy


class JobCategory(scrapy.Item):
    category_name = scrapy.Field()
    vacancies = scrapy.Field()


class JobVacancy(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    date_created = scrapy.Field()
    vacancy_name = scrapy.Field()
    description = scrapy.Field()
    payment_type = scrapy.Field()
    payment_value = scrapy.Field()
    tags = scrapy.Field()
