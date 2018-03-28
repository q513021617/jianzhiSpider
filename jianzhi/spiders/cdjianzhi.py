# -*- coding: utf-8 -*-

# 58同城兼职 spider
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianzhi.items import JianzhiItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
class CdjianzhiSpider(CrawlSpider):
    name = 'cdjianzhi'
    allowed_domains = ['cd.58.com']
    page=1

    url="http://cd.58.com/jianzhi/1/pn"+str(page)+"/?key=%E5%91%A8%E6%9C%AB%E5%85%BC%E8%81%8C&cmcskey=%E5%91%A8%E6%9C%AB%E5%85%BC%E8%81%8C"
    start_urls = [url]


    def deal_span(self,text):
        soup = BeautifulSoup(text)
        text=soup.span.get_text()
        a=""
        if soup.a:
            a=soup.a.get_text()
        return text+a

    def parse(self,response):
        links=response.xpath('//div[@class="left"]/div[@class="items"]/div[@class="item clearfix"]/div[@class="item1"]/h2/a/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parse_item)
        self.page += 1
        print "loading page:" + str(self.page)
        if self.page<5:
            yield scrapy.Request("http://cd.58.com/jianzhi/1/pn"+str(self.page)+"/?key=%E5%91%A8%E6%9C%AB%E5%85%BC%E8%81%8C&cmcskey=%E5%91%A8%E6%9C%AB%E5%85%BC%E8%81%8C",callback=self.parse)

    def parse_item(self,response):
        item=JianzhiItem()
        item['platform'] = "58"
        item['title']=response.xpath('//div[@class="info"]/div/h1/text()').extract()
        item['money']=response.xpath('//div[@class="info"]/div[@class="price"]/span/text()').extract()[0]
        item['content']=""
        item['address'] = ""
        nameList=response.xpath('//div[@class="info"]/div[@class="zpinfo"]/ul/li/div/i/text()').extract()
        for i in range(0,4):
            if nameList[i]:
                item['content']+=nameList[i]+self.deal_span(response.xpath('//div[@class="info"]/div[@class="zpinfo"]/ul/li/div/span').extract()[i])+" "

        item['detailUrl']=response.url
        yield item

    page+=1
    print "loading page:"+str(page)