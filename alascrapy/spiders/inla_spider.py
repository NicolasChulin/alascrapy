from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from alascrapy.items import *
from urllib import unquote
from scrapy import log,Spider,Request
import re
from alascrapy.dblink import Pydb

import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='inla.log',
    filemode='w')


class InlaLawyerSpider(Spider):
    name = 'inlalawyer'
    # allowed_domains = ['chineseinla.com']
    # start_urls = ['http://www.chineseinla.com/lawyer/task_list/catid_2.html']
    start_urls = [
        # 'http://www.chineseinla.com/company.html', # Los Angeles
        # 'http://lv.nychinaren.com/company.html',  # Las Vegas
        # 'http://sd.nychinaren.com/company.html',  # Santiago

        # 'http://www.seattlechinaren.com/company.html', # Seattle
        # 'http://pa.nychinaren.com/company.html',  # Philadelphia
        # 'http://chicago.nychinaren.com/company.html'  # Chicago
        # 'http://tx.nychinaren.com/company.html', # Houston
        # 'http://atlanta.nychinaren.com/company.html', # Atlanta

        'http://www.chineseinsfbay.com/company.html', # San Francisco fobiden
        'http://www.nychinaren.com/company.html'  # New York fobiden

        # 'http://boston.nychinaren.com/company.html', # Boston
        # 'http://hi.nychinaren.com/company.html' # Hawaii
        # 'http://dallas.nychinaren.com/company.html', # Dallas
        # 'http://florida.nychinaren.com/company.html', # Florida
        # 'http://van.nychinaren.com/company.html', # Vancouver
        # 'http://dc.nychinaren.com/company.html', # dahuafu
        # 'http://oz.nychinaren.com/company.html', # Sydney
    ]
    cityDic = {
        'chineseinla.com':{
            'city':'Los Angeles',
            'host':'http://www.chineseinla.com'
        },
        'lv.nychinaren.com':{
            'city':'Las Vegas',
            'host':'http://lv.nychinaren.com'
        },
        'chineseinsfbay.com':{
            'city':'San Francisco',
            'host':'http://www.chineseinsfbay.com'
        },
        'www.chineseinsfbay.com':{
            'city':'San Francisco',
            'host':'http://www.chineseinsfbay.com'
        },
        'sd.nychinaren.com':{
            'city':'Santiago',
            'host':'http://sd.nychinaren.com'
        },
        'nychinaren.com':{
            'city':'New York',
            'host':'http://www.nychinaren.com'
        },
        'www.nychinaren.com':{
            'city':'New York',
            'host':'http://www.nychinaren.com'
        },
        'chicago.nychinaren.com':{
            'city':'Chicago',
            'host':'http://chicago.nychinaren.com'
        },
        'pa.nychinaren.com':{
            'city':'Philadelphia',
            'host':'http://pa.nychinaren.com'
        },
        'www.seattlechinaren.com':{
            'city':'Seattle',
            'host':'http://www.seattlechinaren.com'
        },
        'boston.nychinaren.com':{
            'city':'Boston',
            'host':'http://boston.nychinaren.com'
        },
        'tx.nychinaren.com':{
            'city':'Houston',
            'host':'http://boston.nychinaren.com'
        },
        'hi.nychinaren.com':{
            'city':'Hawaii',
            'host':'http://hi.nychinaren.com'
        },
        'atlanta.nychinaren.com':{
            'city':'Atlanta',
            'host':'http://atlanta.nychinaren.com'
        },
        'dallas.nychinaren.com':{
            'city':'Dallas',
            'host':'http://dallas.nychinaren.com'
        },
        'florida.nychinaren.com':{
            'city':'Florida',
            'host':'http://florida.nychinaren.com'
        },
        'van.nychinaren.com':{
            'city':'Vancouver',
            'host':'http://van.nychinaren.com'
        },
        'dc.nychinaren.com':{
            'city':'dahuafu',
            'host':'http://dc.nychinaren.com'
        },
        'oz.nychinaren.com':{
            'city':'Sydney',
            'host':'http://oz.nychinaren.com'
        }
    }

    def from_url_get_id(self,url):
        urls = url.split('id_')
        ids  =  urls[1].split('/')
        return ids[0]


    def parse(self,response):
        lis = response.xpath("//*[@id='nav']/li")
        navas = lis.xpath(".//div[@class='category_list']/dl/dd/a/@href").extract()
        cityinfo = self.cityDic[response.meta['download_slot']]
        for n in navas:
            url = cityinfo['host']+n
            yield Request(url=url, callback=self.parse_pages)


    def parse_pages(self,response):
        lawyers_pos = response.xpath("//*[@id='category_content']/dl[@class='regular_company']")
        cityinfo = self.cityDic[response.meta['download_slot']]


        for lawyer in lawyers_pos:
            try:
                item = BusinessItem()

                atag = lawyer.xpath(".//dt/div")
                url = atag.xpath(".//a[1]/@href").extract()[0].encode('utf8')
                url = unquote(url)
                name = atag.xpath(".//a[1]/@title").extract()[0].encode('utf8')
                user_id = self.from_url_get_id(url)
                item['url'] = cityinfo['host']+url
                item['name'] = name
                item['user_id'] = user_id
                item['city'] = cityinfo['city']

                infos = lawyer.xpath(".//dd/div[@class='tag_text']")
                if len(infos) != 0:

                    if len(infos.xpath(".//div[@class='list_phone']")) != 0:
                        phones = infos.xpath(".//div[@class='list_phone']/text()").extract()
                        phone = ';'.join(phones).strip().encode('utf8')
                        item['phone'] = phone

                    category = infos.xpath(".//div[@class='list_category']")
                    if len(category) != 0:
                        main_category = category.xpath(".//a[1]/text()").extract()[0].encode('utf8')
                        sub_category = ';'.join(category.xpath(".//span[@class='list_tag']/a/text()").extract()).encode('utf8')
                        item['main_category'] = main_category
                        item['sub_category'] = sub_category

                    addr = infos.xpath(".//div[@class='address_list_block']/div[@class='adress_text']")
                    if len(addr)!=0:
                        address = addr.xpath(".//a/text()").extract()[0].encode('utf8')
                        item['address'] = address


                self.log('=====>url:%s......Done' % url,level=log.INFO)
                yield item
            except Exception as e:
                self.log('=====>url:%s......Error' % url,level=log.WARNING)
                yield item


        page_box = response.xpath("//*[@id='category_content']/div/div[@class='tag_pagination_box']/div[@class='tpb_box']")
        if len(page_box) != 0:
            page_box = page_box[-2]
            if len(page_box.xpath(".//a")) != 0:
                url = page_box.xpath(".//a[1]/@href").extract()[0]
                if url:
                    yield Request(url=cityinfo['host']+url, callback=self.parse_pages)




class ExperSprider(Spider):

    name = 'exper'
    cityDic = {
        'www.chineseinla.com':{
            'city':'Los Angeles',
            'host':'http://www.chineseinla.com'
        },
        'lv.nychinaren.com':{
            'city':'Las Vegas',
            'host':'http://lv.nychinaren.com'
        },
        'www.chineseinsfbay.com':{
            'city':'San Francisco',
            'host':'http://www.chineseinsfbay.com'
        },
        'sd.nychinaren.com':{
            'city':'Santiago',
            'host':'http://sd.nychinaren.com'
        },
        'www.nychinaren.com':{
            'city':'New York',
            'host':'http://www.nychinaren.com'
        },
        'chicago.nychinaren.com':{
            'city':'Chicago',
            'host':'http://chicago.nychinaren.com'
        },
        'pa.nychinaren.com':{
            'city':'Philadelphia',
            'host':'http://pa.nychinaren.com'
        },
        'www.seattlechinaren.com':{
            'city':'Seattle',
            'host':'http://www.seattlechinaren.com'
        },
        'boston.nychinaren.com':{
            'city':'Boston',
            'host':'http://boston.nychinaren.com'
        },
        'tx.nychinaren.com':{
            'city':'Houston',
            'host':'http://boston.nychinaren.com'
        },
        'hi.nychinaren.com':{
            'city':'Hawaii',
            'host':'http://hi.nychinaren.com'
        },
        'atlanta.nychinaren.com':{
            'city':'Atlanta',
            'host':'http://atlanta.nychinaren.com'
        },
        'dallas.nychinaren.com':{
            'city':'Dallas',
            'host':'http://dallas.nychinaren.com'
        },
        'florida.nychinaren.com':{
            'city':'Florida',
            'host':'http://florida.nychinaren.com'
        },
        'van.nychinaren.com':{
            'city':'Vancouver',
            'host':'http://van.nychinaren.com'
        },
        'dc.nychinaren.com':{
            'city':'dahuafu',
            'host':'http://dc.nychinaren.com'
        },
        'oz.nychinaren.com':{
            'city':'Sydney',
            'host':'http://oz.nychinaren.com'
        }
    }

    def get_email(self,lists):
        listcont = ';'.join(lists)
        emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",listcont)
        if len(emails) != 0:
            return ';'.join(emails)
        else:
            return None

    def from_url_get_id(self,url):
        urls = url.split('id_')
        ids  =  urls[1].split('/')
        return ids[0]

    def start_requests(self):
        num = 51071
        # liss = [34363]
        table = 'inla'
        pydb = Pydb()
        for n in range(51072,74828):
            lis = pydb.filter(table,{'id':n})
            if len(lis) == 1:
                yield Request(url=lis[0]['url'], callback=self.parse,meta={'id':n})


    def parse(self,response):
        aid = response.meta['id']
        try:
            item = UpinlaItem()
            cityinfo = self.cityDic[response.meta['download_slot']]
            user_id = self.from_url_get_id(response.url)
            item['user_id'] = user_id
            item['city'] = cityinfo['city']

            citems = []
            if len(response.xpath("//*[@class='map_title_box']/div[@class='company_item']")) != 0:
                citems = response.xpath("//*[@class='map_title_box']/div[@class='company_item']/text()").extract()

            texts = response.xpath("//*[@id='company_memo']")
            if len(texts) != 0:
                text = texts.extract()[0]
                citems.append(text)

            item['email'] = self.get_email(citems) if len(citems)!=0 else None

            self.log('=====>id:%s......Done' % aid,level=log.INFO)
            logging.info("id:%s,email:%s,user_id:%s,city:%s" % (aid,item['email'],item['user_id'],item['city']))
            yield item

        except Exception as e:
            item['email'] = None
            logging.info("id:%s,email:%s,user_id:%s,city:%s" % (aid,item['email'],item['user_id'],item['city']))
            self.log('=====>id:%s......Error' % aid,level=log.INFO)
            yield item


class FillEmptySpider(Spider):

    name = 'fillempty'

    def get_phone(phoneStr):
        phoneStr = str(phoneStr).strip().replace(' ','')
        if not phoneStr or phoneStr == 'None':
            return 'None'

        phoneStr = re.sub(r'[\.\-\(\)）（]+','#',phoneStr)

        relist = [
            r"(1#[0-9]{3}#[0-9]{3}#[0-9]{4})",
            r"([0-9]{3}#[0-9]{3}#[0-9]{4})",
            r"([0-9]{10,11})"
        ]

        phones = []
        for res in relist:
            result = re.findall(res,phoneStr)
            phones.extend(result)
            for s in result:
                phoneStr.replace(s,'')

        return ';'.join(phones).replace('#','')

    def start_requests(self):
        table = 'inla'
        pydb = Pydb()
        sql = "SELECT id,url FROM %s WHERE ISNULL(phone) or phone=''" % table
        inlaitems = pydb.query(sql)
        for litem in inlaitems:
            yield Request(url=litem['url'], callback=self.parse,meta={'id':litem['id']})


    def parse(self,response):
        item = UpinlaItem()
        item['main_category'] = ''
        item['sub_category'] = ''
        item['phone'] = ''
        item['aid'] = response.meta['id']
        try:
            item['main_category'] = response.xpath("//*[@class='pathway']/a[3]/text()").extract()[0].encode('utf8')
            comps = response.xpath("//*[@class='map_title_box']")

            subpos = comps.xpath(".//div[contains(@style,'background: url(/templates/horse/images/company_detail.png) no-repeat 0px -205px')]")
            if len(subpos) != 0:
                item['sub_category'] = ';'.join(subpos.xpath(".//a/text()").extract()).encode('utf8')

            phonepos = comps.xpath(".//div[contains(@style,'background: url(/templates/horse/images/company_detail.png) no-repeat 0px -234px')]/text()")
            if len(phonepos) != 0:
                item['phone'] = ';'.join(phonepos.extract()).strip().encode('utf8')
                item['phone'] = self.get_phone(item['phone'])

            yield item

        except Exception as e:
            logging.info("error....url:%s" % item['url'])
            yield item


