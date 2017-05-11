from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from alascrapy.items import *
from urllib import unquote
from scrapy import log,Spider,Request


class InlaLawyerSpider(Spider):
    name = 'inlalawyer'
    # allowed_domains = ['chineseinla.com']
    # start_urls = ['http://www.chineseinla.com/lawyer/task_list/catid_2.html']
    start_urls = [
        # 'http://www.chineseinla.com/company.html', # Los Angeles
        'http://lv.nychinaren.com/company.html',  # Las Vegas
        'http://www.chineseinsfbay.com/company.html', # San Francisco
        'http://sd.nychinaren.com/company.html',  # Santiago
        'http://www.nychinaren.com/company.html'  # New York
        'http://chicago.nychinaren.com/company.html'  # Chicago
        'http://pa.nychinaren.com/company.html',  # Philadelphia
        'http://www.seattlechinaren.com/company.html', # Seattle
        'http://boston.nychinaren.com/company.html', # Boston
        'http://tx.nychinaren.com/company.html', # Houston
        'http://hi.nychinaren.com/company.html' # Hawaii
        'http://atlanta.nychinaren.com/company.html', # Atlanta
        'http://dallas.nychinaren.com/company.html', # Dallas
        'http://florida.nychinaren.com/company.html', # Florida
        'http://van.nychinaren.com/company.html', # Vancouver
        'http://dc.nychinaren.com/company.html', # dc
        'http://oz.nychinaren.com/company.html', # Sydney
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
        'sd.nychinaren.com':{
            'city':'Santiago',
            'host':'http://sd.nychinaren.com'
        },
        'nychinaren.com':{
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
        'seattlechinaren.com':{
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
            # print(url)
            yield Request(url=url, callback=self.parse_pages)


    def parse_pages(self,response):
        lawyers_pos = response.xpath("//*[@id='category_content']/dl[@class='regular_company']")
        cityinfo = self.cityDic[response.meta['download_slot']]
        # print(response.meta['download_slot'])
        # print(cityinfo)

        for lawyer in lawyers_pos:
            try:
                item = InlaItem()

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
                        phone = infos.xpath(".//div[@class='list_phone']/text()").extract()[0].encode('utf8')
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





# class InlaLawyerSpider(Spider):
#     name = 'inlalawyer'
#     allowed_domains = ['chineseinla.com']
#     start_urls = ['http://www.chineseinla.com/lawyer/task_list/catid_2.html']

#     def from_url_get_id(self,url):
#         urls = url.split('id_')
#         ids  =  urls[1].split('/')
#         return ids[0]

#     def parse(self,response):
#         lawyers_pos = response.xpath("//*[@id='category_content']/dl[@class='regular_company']")
#         for lawyer in lawyers_pos:
#             try:
#                 atag = lawyer.xpath(".//dt/div")
#                 url = atag.xpath(".//a[1]/@href").extract()[0].encode('utf8')
#                 url = unquote(url)
#                 name = atag.xpath(".//a[1]/@title").extract()[0].encode('utf8')
#                 user_id = self.from_url_get_id(url)
#                 self.log('=====>url:%s......Done' % url,level=log.INFO)

#                 infos = lawyer.xpath(".//dd/div[@class='tag_text']")
#                 address = infos.xpath(".//div/div[@class='adress_text']/a[1]/text()").extract()[0].encode('utf8')
#                 phone = infos.xpath(".//div[@class='list_phone']/text()").extract()[0].encode('utf8')

#                 category = infos.xpath(".//div[@class='list_category']")
#                 main_category = category.xpath(".//a[1]/text()").extract()[0].encode('utf8')
#                 sub_category = ';'.join(category.xpath(".//span[@class='list_tag']/a/text()").extract()).encode('utf8')

#                 item = InlaItem()
#                 item['url'] = 'http://www.chineseinla.com'+url
#                 item['name'] = name
#                 item['user_id'] = user_id
#                 item['address'] = address
#                 item['phone'] = phone
#                 item['main_category'] = main_category
#                 item['sub_category'] = sub_category
#                 yield item
#             except Exception as e:
#                 continue

#         page_box = response.xpath("//*[@id='category_content']/div/div[@class='tag_pagination_box']/div[@class='tpb_box']")[-2]
#         if len(page_box.xpath(".//a")) != 0:
#             url = page_box.xpath(".//a[1]/@href").extract()[0]
#             text = page_box.xpath(".//a[1]/text()").extract()[0]
#             if url:
#                 yield Request(url='http://www.chineseinla.com'+url, callback=self.parse)



# class baikeSpider(CrawlSpider):

#     name = 'baike_python'
#     allowed_domains = ['baike.baidu.com']
#     start_urls = ['http://baike.baidu.com/item/scrapy']
#     rules = [Rule(LinkExtractor(allow=['/item/\S+']), callback='parse_torrent')]

#     def toUtf(self,str):
#         # return str.decode('unicode_escape')
#         return str.encode('utf8')

#     def parse_torrent(self, response):
#         # print(response)

#         print('===============meta==>')
#         print('domain:%s' % response.meta['download_slot'])
#         torrent = BaikePythonItem()
#         torrent['url'] = unquote(self.toUtf(response.url))
#         print('url:%s' % torrent['url'])

#         # torrent['name'] = self.toUtf(response.xpath("//title/text()").extract()[0])
#         # torrent['description'] = self.toUtf(response.css("meta[name=description]::attr(content)").extract()[0])
#         return torrent
