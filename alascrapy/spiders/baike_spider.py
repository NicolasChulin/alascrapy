from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from alascrapy.items import *
from urllib import unquote
from scrapy import log,Spider,Request
import re


class baikeSpider(CrawlSpider):

    name = 'baike'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/item/scrapy']
    rules = [Rule(LinkExtractor(allow=['/item/\S+']), callback='parse_torrent')]

    def toUtf(self,str):
        return str.encode('utf8')

    def parse_torrent(self, response):
        torrent = BaikePythonItem()
        torrent['url'] = unquote(self.toUtf(response.url))
        torrent['name'] = self.toUtf(response.xpath("//title/text()").extract()[0])
        torrent['description'] = self.toUtf(response.css("meta[name=description]::attr(content)").extract()[0])
        return torrent
