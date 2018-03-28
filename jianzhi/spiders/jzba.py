# -*- coding: utf-8 -*-

# 兼职猫兼职 spider
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianzhi.items import JianzhiItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
class jzba(CrawlSpider):
    name = 'jzba'
    allowed_domains = ['cd.jianzhiba.net']
    page=1

    url="http://cd.jianzhiba.net/pixian/jianzhi/p"+str(page)+"/"
    start_urls = [url]


    def deal_span(self,text):
        soup = BeautifulSoup(text)
        text=soup.span.get_text()
        a=""
        if soup.a:
            a=soup.a.get_text()
        return text+a

    def parse(self,response):
        links=response.xpath('//div[@class="left fl"]/div[@class="left-part"]/div[@class="parttime-list"]/ul/li/span/a/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parse_item)
        self.page += 1
        print "loading page:" + str(self.page)
        if self.page<5:
            yield scrapy.Request("http://http://cd.jianzhiba.net/pixian/jianzhi/p"+str(self.page)+"/",callback=self.parse)

    def parse_item(self,response):
        item=JianzhiItem()
        item['platform']="jzba"
        item['title']=response.xpath('//div[@class="left fl"]/div[@class="left-part"]/div[@class="title"]/span/h1/text()').extract()
        item['money']=response.xpath('//div[@class="left fl"]/div[@class="left-part"]/div[@class="article-main"]/dl/dd/text()').extract()[1]
        #
        item['content']=response.xpath('//div[@class="stu-main clearfix marg"]/div[@class="left fl"]/div[@class="left-part"]/div[@class="article-main"]/text()').extract()[1]+response.xpath('//div[@class="left fl"]/div[@class="left-part"]/div[@class="article-main"]/text()').extract()[2]
        #
        item['address'] = response.xpath('//div[@class="left fl"]/div[@class="left-part"]/div[@class="article-main"]/dl/dd/text()').extract()[5]

        item['detailUrl']=response.url
        yield item

    page+=1
    print "loading page:"+str(page)