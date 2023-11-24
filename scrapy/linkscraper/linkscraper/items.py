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
    nhs_url = scrapy.Field()
    url = scrapy.Field()
