from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from alascrapy.items import *
from urllib import unquote
from scrapy import log,Spider,Request
import re

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

class UsalifeSpider(Spider):

    name = 'usalife'
    start_urls = [
        'http://www.usalifeonline.com/f/index.php?choose_cityID=1',
        'http://www.usalifeonline.com/f/index.php?choose_cityID=2',
        'http://www.usalifeonline.com/f/index.php?choose_cityID=3',
    ]
    domain = 'http://www.usalifeonline.com'
    citys = ['','East','South','West']

    def get_url_params(self,url):
        url = url.lower()
        urls = url.split('?')
        items = urls[1].split('&')
        params = {}
        for t in items:
            ts = t.split('=')
            params[ts[0]] = ts[1]

        return params

    def get_email(self,lists):
        listcont = ';'.join(lists)
        emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",listcont)
        if len(emails) != 0:
            return ';'.join(emails)
        else:
            return None


    def parse(self,response):
        mUrlsPos = response.xpath("//*[@class='newjs']/div[contains(@class,'listsort')]")[8:]
        murls = mUrlsPos.xpath(".//div[@class='moresort']/div")
        for mpos in murls:
            url = mpos.xpath("./a[1]/@href").extract()[0]
            yield Request(url=url,callback=self.parse_main_category)

    def parse_main_category(self,response):
        tds = response.xpath("//div[@class='fenleicontmxx']")
        if len(tds) != 0:
            for t in tds:
                url = t.xpath(".//*[@class='xxtitle']/a[1]/@href").extract()[0]
                yield Request(url=url,callback=self.parse_page_detail)

            # next page
            pagePos = response.xpath("//*[@class='page']")
            if len(pagePos.xpath(".//a")) != 0:
                allpage = pagePos.xpath(".//a[@href='#']/text()")[-1].extract().split('/')[1]
                curpage = pagePos.xpath(".//a[@href='#'][1]/font/text()").extract()[0]
                if curpage != allpage:
                    nexturl = pagePos.xpath(".//a/@href").extract()[-3]
                    yield Request(url=nexturl,callback=self.parse_main_category)
        else:
            yield {}

    def parse_page_detail(self,response):
        item = BusinessItem()
        params = self.get_url_params(response.url)
        item['url'] = response.url.replace('//f','/f')
        item['city'] = self.citys[int(params['city_id'])]
        item['user_id'] = params['id']

        item['name'] = response.xpath("//*[@class='hytitlez']/text()").extract()[0].encode('utf8')

        categorys = response.xpath("//*[@class='bjishiwz']/a/text()").extract()
        item['main_category'] = categorys[0].strip().encode('utf8')
        item['sub_category'] = categorys[1].strip().encode('utf8')

        phone = response.xpath("//*[@class='hytelt']/text()").extract()
        item['phone'] = phone[0] if len(phone)!=0 else ''
        address = response.xpath("//*[@class='hydzt']/text()").extract()
        item['address'] = address[0] if len(address)!=0 else ''

        infos = response.xpath("//*[@class='hymc1']").extract()
        email = self.get_email(infos)
        item['email'] = email if email else ''

        yield item





