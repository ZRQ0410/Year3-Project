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
        # drop duplicate GPs
        # when gp names are the same & postcode are the same
        adapter = ItemAdapter(item)
        gp_code_pair = (adapter['gp'], adapter['postcode'])
        if gp_code_pair in self.stored_data:
            raise DropItem(f"Duplicate pair found: {item}")
        else:
            self.stored_data.add((adapter['gp'], adapter['postcode']))
            return item


class SaveToMySQLPipeline:
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
        CREATE TABLE IF NOT EXISTS gp_table(
            id int NOT NULL auto_increment,
            gp VARCHAR(255),
            locname VARCHAR(255),
            postcode VARCHAR(255),
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        # insert
        self.cur.execute("""INSERT INTO gp_table(gp, locname, postcode) values (%s, %s, %s)""",
                         (item['gp'], item['locname'], item['postcode']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # close cursor and connection
        self.cur.close()
        self.conn.close()
