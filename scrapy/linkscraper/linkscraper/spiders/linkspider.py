import csv
import scrapy
import time
import random
from fake_useragent import UserAgent
from ..items import GPItem
import re


class LinkspiderSpider(scrapy.Spider):
    name = "linkspider"
    allowed_domains = ["www.nhs.uk"]
    ua = UserAgent()
    start_urls = ["https://www.nhs.uk"]

    def parse(self, response):
        # get all gp info: names, nhs overview links
        with open('../data/nhslinks_cleaned.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
            # delete the header: gp, postcode, nhs_url
            data.pop(0)

        for info in data:
            # gp name: info[0], postcode: info[1], nhs overview link: info[2]
            time.sleep(random.uniform(0.2, 0.5))

            # if data does not contain an overview url
            if info[2] == '':
                gp_item = GPItem()
                gp_item['gp'] = info[0]
                gp_item['postcode'] = info[1]
                gp_item['nhs_url'] = None
                gp_item['url'] = None
                gp_item['state'] = None
                yield gp_item
            # if has an overview url
            else:
                yield response.follow(info[2], callback=self.parse_overview, cb_kwargs={'gp': info[0], 'postcode': info[1], 'nhs_url': info[2]}, headers={"User-Agent": self.ua.random}, dont_filter=True)

    def process_name(self, name):
        """
        Convert all gp names into the same format.
        1) remove all punctuations, in case some punctuations have subtle difference, eg. '-' (hyphen) and '–' (en dash)
        2) ignore space
        3) convert to lower case
        """
        name_cleaned = re.sub(r'[^\w\s]', '', name).replace(' ', '').lower()
        return name_cleaned

    def parse_overview(self, response, gp, postcode, nhs_url):
        gp_item = GPItem()
        title = response.css(".nhsuk-caption-xl::text").get().strip()
        addr = response.css(
            '[id="address_panel_address"]::text').extract()[-1].strip()
        # convert two strings into the same format (easier for comparison)
        title_str = self.process_name(title)
        name_str = self.process_name(gp)

        # compare name & postcode with  title and address on the overview page
        # if information matches => correct overview page
        if (title_str == name_str and addr == postcode):
            try:
                url = response.css(
                    '[id="contact_info_panel_website_link"]').attrib['href']
                state = 1
            # if overview page does not provide gp url
            except Exception:
                url = None
                state = 0

            gp_item['gp'] = gp
            gp_item['postcode'] = postcode
            gp_item['nhs_url'] = nhs_url
            gp_item['url'] = url
            gp_item['state'] = state
            yield gp_item

        # if the page shows a different name/postcode => wrong overview page
        # set nhs_url and other related info to None
        else:
            gp_item['gp'] = gp
            gp_item['postcode'] = postcode
            gp_item['nhs_url'] = None
            gp_item['url'] = None
            gp_item['state'] = None
            yield gp_item
