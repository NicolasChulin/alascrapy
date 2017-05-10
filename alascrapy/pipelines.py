# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from datetime import datetime
from alascrapy.dblink import Pydb
from scrapy.exceptions import DropItem

class MysqlWriterPipeline(object):

    def __init__(self):
        self.pydb = Pydb()

    def process_item(self, item, spider):
        table = 'inla'
        if self.pydb.get_count(table,{'user_id':item['user_id']}) > 0:
            raise DropItem('Duplicate item found: %s' % item['url'])
        else:
            item.update({'created_at':datetime.now()})
            self.pydb.create(table,item)
            return item

    # def process_item(self, item, spider):
    #     table = 'baike'
    #     if self.pydb.get_count(table,{'url':item['url']}) > 0:
    #         raise DropItem('Duplicate item found: %s' % item['url'])
    #     else:
    #         item.update({'created_at':datetime.now()})
    #         self.pydb.create(table,item)
    #         return item