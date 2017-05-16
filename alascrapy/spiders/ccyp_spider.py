from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from alascrapy.items import *
from urllib import unquote
from scrapy import log,Spider,Request
import re

class CcypSpider(Spider):

    name = 'ccyp'
    start_urls = [
        # 'http://www.ccyp.com/home_SCA_area/index',
        'http://www.ccyp.com/home_NCA_area/index'
    ]
    domain = 'http://www.ccyp.com'

    def parse(self,response):
        mUrlsPos = response.xpath("//*[@id='second-nav']/nav/div/div[2]/div[1]/div[2]/div/div[@class='col-xs-1']")
        for mpos in mUrlsPos:
            url = mpos.xpath("./a[1]/@href").extract()[0].encode('utf8')
            yield Request(url=self.domain+url,callback=self.parse_main_category)

    def parse_main_category(self,response):
        tds = response.xpath("//table[contains(@class,'table list-category')]/tr/td[1]")
        for t in tds:
            url = t.xpath(".//a[1]/@href").extract()[0].encode('utf8')
            yield Request(url=self.domain+url,callback=self.parse_sub_category)

    def parse_sub_category(self,response):
        listPos = response.xpath("//div[contains(@class,'row-fluid yellow-listing')]/div/div[@class='list-result']/div/div/div/div/div[@class='info-left']")
        for lis in listPos:
            url = lis.xpath(".//h1[1]/a[1]/@href").extract()[0].encode('utf8')
            yield Request(url=self.domain+url,callback=self.parse_page_detail)

        nextpage = response.xpath("//*[@class='PagedList-skipToNext']")
        if len(nextpage) != 0:
            url = nextpage.xpath(".//a[1]/@href").extract()[0].encode('utf8')
            yield Request(url=self.domain+url,callback=self.parse_sub_category)


    def parse_page_detail(self,response):
        item = CcypItem()
        item['name'] = response.xpath("//*[@class='header-banner']/h2/span/text()").extract()[0].encode('utf8')
        item['url'] = response.url.encode('utf8')
        item['city'] = 'San Francisco'
        # item['city'] = 'Los Angeles'

        categorys = response.xpath("//*[@class='breadcrumb']/li/a/text()").extract()
        item['main_category'] = categorys[-2].strip().encode('utf-8')
        item['sub_category'] = categorys[-1].strip()[3:].encode('utf-8')

        urls = response.url.split('/')
        item['user_id'] = urls[-2]

        infobox = response.xpath("//*[@id='pnlbranch']/div")
        if len(infobox) != 0:
            addrbox = infobox[0].xpath(".//dl/dd[@itemprop='address']")
            if len(addrbox) != 0:
                item['address'] = ' '.join(addrbox[0].xpath(".//span/text()").extract()).encode('utf8')

            item['phone'] = ';'.join(infobox.xpath(".//dl/dd/span[@itemprop='telephone']/text()").extract()).encode('utf8')

        entrypos = response.xpath(".//a[@class='ow']/@href")
        item['website'] = entrypos.extract()[0].encode('utf8') if len(entrypos) else '';
        yield item






















