# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            passward='',
            database='nhs'
        )

        # create cursor
        self.cur = self.conn.cursor()

        # create nhs table if not exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS nhs(
            id int NOT NULL auto_increment,
            gp VARCHAR(255),
            locname VARCHAR(255),
            url VARCHAR(255)
        )
        """)

    def process_item(self, item, spider):
        # insert
        self.cur.execute("""INSERT INTO nhs(gp, locname, url) values (%s, %s, %s)""",
                         (item['gp'], item['locame'], item['url']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # close cursor and connection
        self.cur.close()
        self.conn.close()
