import scrapy
import random
# from items import GPItem


class NhsspiderSpider(scrapy.Spider):
    name = "nhsspider"
    allowed_domains = ["www.nhs.uk"]
    start_urls = [
        "https://www.nhs.uk/service-search/other-services/GP/Location/Places/Z/4"]
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
    ]

    def parse(self, response):
        places = response.css('.fclist-section li a')
        for place in places:
            location_url = place.attrib['href']
            yield response.follow(location_url, callback=self.parse_place_page, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

        # from page 1 to last page
        has_next_page = response.css('.next a')
        if has_next_page:
            next_page_url = 'https://www.nhs.uk' + has_next_page.attrib['href']
            yield response.follow(next_page_url, callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

        # from 'A' to 'Z'
        letter = response.css('.fclist-section h2::text').get()
        if letter != 'Z':
            letter = chr(ord(letter) + 1)
            next_letter_url = 'https://www.nhs.uk/service-search/other-services/GP/Location/Places/' + letter + '/4'
            yield response.follow(next_letter_url, callback=self.parse, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})

    def parse_place_page(self, response):
        gps = response.css('.fctitle a ::text')
        locname = response.css('[id="locname"]::text').extract()

        # gp_item = GPItem()
        for gp in gps:
            yield {
                'gp': gp.get(),
                'locname': locname
            }
            # gp_item['gp'] = gp.get()
            # gp_item['locname'] = locname
            # yield gp_item

        has_next_page = response.css('.next a')
        if has_next_page:
            next_page_url = 'https://www.nhs.uk' + has_next_page.attrib['href']
            yield response.follow(next_page_url, callback=self.parse_place_page, headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]})
