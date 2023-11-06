# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:
    def __init__(self):
        self.stored_data = set()

    def process_item(self, item, spider):
        # drop duplicate rows
        # there can be multiple GPs with the same names in the same place
        # only keep one unique GP for each place
        adapter = ItemAdapter(item)
        gp_loc_pair = (adapter['gp'], adapter['locname'])
        if gp_loc_pair in self.stored_data:
            raise DropItem(f"Duplicate pair found: {item}")
        else:
            self.stored_data.add((adapter['gp'], adapter['locname']))
            return item


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nhs'
        )

        # create cursor
        self.cur = self.conn.cursor()

        # create nhs table if not exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS gp_loc(
            id int NOT NULL auto_increment,
            gp VARCHAR(255),
            locname VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        # insert
        self.cur.execute("""INSERT INTO gp_loc(gp, locname) values (%s, %s)""",
                         (item['gp'], item['locname']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # close cursor and connection
        self.cur.close()
        self.conn.close()
