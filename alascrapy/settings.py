# -*- coding: utf-8 -*-

# Scrapy settings for alascrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#


BOT_NAME = 'alascrapy'

SPIDER_MODULES = ['alascrapy.spiders']
NEWSPIDER_MODULE = 'alascrapy.spiders'


DEFAULT_DB = {
    'NAME': 'alascrapy',
    'HOST': 'localhost',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD': 'root'
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'alascrapy (+http://www.yourdomain.com)'


USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
COOKIES_ENABLED = False
DOWNLOAD_DELAY = 0.3


ITEM_PIPELINES = {
    # 'alascrapy.pipelines.MysqlWriterPipeline': 800,
    'alascrapy.pipelines.MysqlUpdatePipeline': 800,
}


