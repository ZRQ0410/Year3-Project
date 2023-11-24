# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# from urllib.request import urlopen
# from urllib.error import URLError, HTTPError
import requests
from requests.exceptions import ConnectionError


class LinkscraperPipeline:
    def process_item(self, item, spider):
        return item


class ValidateURLPipeline:
    def process_item(self, item, spider):
        # if collected the main website url, check whether the url is working
        adapter = ItemAdapter(item)
        url = adapter['url']

        if url != "notfound":
            # try:
            #     response = urlopen(adapter['url'])
            # except HTTPError as e:
            #     print('Error code:', e.code, e.reason)
            #     adapter['url'] = 'HTTPError'
            # except URLError as e:
            #     print('Reason:', e.reason)
            #     adapter['url'] = 'URLError'
            # return item
            try:
                request = requests.get(url)
            except ConnectionError:
                print('Website does not exist')
                adapter['url'] = 'failed'
        return item
