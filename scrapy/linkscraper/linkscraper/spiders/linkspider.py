import csv
import scrapy
import time
import random
from fake_useragent import UserAgent
from ..items import GPItem


class LinkspiderSpider(scrapy.Spider):
    name = "linkspider"
    allowed_domains = ["www.nhs.uk"]
    ua = UserAgent()
    start_urls = ["https://www.nhs.uk"]

    def parse(self, response):
        # get all gp info: names, nhs overview links
        with open('../gscraper/cleaned_nhslinks.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
            # delete the header: gp, nhs_url
            data.pop(0)

        for info in data:
            # gp name: info[0], nhs overview link: info[1]
            time.sleep(random.uniform(0.2, 0.5))
            yield response.follow(info[1], callback=self.parse_overview, cb_kwargs={'nhs_url': info[1]}, headers={"User-Agent": self.ua.random})

    def parse_overview(self, response, nhs_url):
        gp_item = GPItem()
        gp = response.css(".nhsuk-caption-xl::text").get().strip()
        try:
            url = response.css(
                '[id="contact_info_panel_website_link"]').attrib['href']
        # for KeyError or any other error
        except Exception:
            url = 'notfound'

        gp_item['gp'] = gp
        gp_item['nhs_url'] = nhs_url
        gp_item['url'] = url
        yield gp_item
