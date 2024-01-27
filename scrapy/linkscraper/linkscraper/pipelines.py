# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import requests
from requests.exceptions import ConnectionError
import mysql.connector


class LinkscraperPipeline:
    def process_item(self, item, spider):
        return item


# class DropWrongPagePipeline:
#     """
#     Drop data if the information is different from the one on the nhs overview page. This means we found the wrong overview page for this gp, hence need to be dropped.
#     """

#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if adapter['nhs_url'] is None:
#             raise DropItem(
#                 f"Found incorrect overview page: {item['gp']}, {item['postcode']}")
#         else:
#             return item


class ValidateURLPipeline:
    """
    If collected the main website url, check whether the url is working.
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter['url']

        if url is not None:
            try:
                request = requests.get(url)
            except ConnectionError:
                print('Website does not exist')
                # if url not working, set state: -1
                adapter['state'] = -1
        return item


class SaveToMySQLPipeline:
    """
    Save to SQL database.
    """

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            # add password
            password='a1292732905',
            database='nhs'
        )

        # create cursor
        self.cur = self.conn.cursor()

        # create nhs table if not exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS url_table(
            id int NOT NULL auto_increment,
            gp VARCHAR(255),
            postcode VARCHAR(255),
            nhs_url TEXT,
            url TEXT,
            state int,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        # insert
        self.cur.execute("""INSERT INTO url_table(gp, postcode, nhs_url, url, state) values (%s, %s, %s, %s, %s)""",
                         (item['gp'], item['postcode'], item['nhs_url'], item['url'], item['state']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # close cursor and connection
        self.cur.close()
        self.conn.close()
