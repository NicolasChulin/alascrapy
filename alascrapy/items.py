# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BaikePythonItem(Item):
    name = Field()
    description = Field()
    url = Field()
    created_at = Field()


class InlaItem(Item):
    name = Field()
    user_id = Field()
    url = Field()
    main_category = Field()
    sub_category = Field()
    email = Field()
    phone = Field()
    fax = Field()
    website = Field()
    address = Field()
    description = Field()
    created_at = Field()

