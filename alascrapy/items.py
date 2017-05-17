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


class UpinlaItem(Item):
    user_id = Field()
    email = Field()
    city = Field()


class BusinessItem(Item):
    name = Field()
    user_id = Field()
    url = Field()
    city = Field()
    main_category = Field()
    sub_category = Field()
    email = Field()
    phone = Field()
    website = Field()
    address = Field()
    created_at = Field()

