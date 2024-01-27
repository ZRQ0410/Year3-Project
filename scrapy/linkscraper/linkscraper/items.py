# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GPItem(scrapy.Item):
    gp = scrapy.Field()
    postcode = scrapy.Field()
    # overview page url
    nhs_url = scrapy.Field()
    # main website url
    url = scrapy.Field()
    # status of website url:
    # 0: url not provided; -1: failed; 1: working
    state = scrapy.Field()
