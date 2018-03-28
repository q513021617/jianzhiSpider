# -*- coding: utf-8 -*-

# 兼客兼职 spider
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianzhi.items import JianzhiItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
class jianke(CrawlSpider):
    name = 'jianke'
    allowed_domains = ['cd.jianke.cc']
    page=1

    url="https://cd.jianke.cc/aj_434_1/"
    start_urls = [url]


    def deal_span(self,text):
        soup = BeautifulSoup(text)
        text=soup.span.get_text()
        a=""
        if soup.a:
            a=soup.a.get_text()
        return text+a

    def parse(self,response):
        links=response.xpath('//div[@class="main clearFloat"]/div[@class="resultWrap fl"]/div[@class="resultContent"]/div[@id="listWrap"]/ul/li/div[@class="modJobListTxt"]/div/a/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parse_item)

        print "loading page:" + str(self.page)

    def parse_item(self,response):
        item=JianzhiItem()
        item['platform']="jianke"
        item['title']=response.xpath('//div[@class="contentWrap"]/div[@class="content"]/div[@class="jobContent"]/div[@class="jobbody"]/div[@class="jobTitleBlock"]/div[@class="title"]/text()').extract()
        item['money']=response.xpath('//div[@class="contentWrap"]/div[@class="content"]/div[@class="jobContent"]/div[@class="jobbody"]/div[@class="jobTitleBlock"]/div[@class="titleTips"]/span[@class="salary"]/text()').extract()[0]
        #
        item['content']=response.xpath('//div[@class="contentWrap"]/div[@class="content"]/div[@class="jobContent"]/div[@class="jobbody"]/div[@class="jobDetail"]/div[@class="jobDetailContent"]/text()').extract()
        #
        item['address'] = response.xpath('//div[@class="contentWrap"]/div[@class="content"]/div[@class="jobContent"]/div[@class="jobbody"]/div[@class="baseInfo"]/div/span/text()').extract()

        item['detailUrl']=response.url
        yield item


    print "loading page:"+str(page)