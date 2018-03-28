# -*- coding: utf-8 -*-

# 斗米兼职 spider
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianzhi.items import JianzhiItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
class doumi(CrawlSpider):
    name = 'doumi'
    allowed_domains = ['www.doumi.com']
    page=1

    url="http://www.doumi.com/cd/pixian/o"+str(page)+"/"
    start_urls = [url]


    def deal_span(self,text):
        soup = BeautifulSoup(text)
        text=soup.span.get_text()
        a=""
        if soup.a:
            a=soup.a.get_text()
        return text+a

    def parse(self,response):
        links=response.xpath('//div[@class="jzList-con w"]/div[@class="jzList-item clearfix"]/div[@class="jzList-txt"]/div[@class="jzList-txt-t"]/h3/a/@href').extract()
        for link in links:
            yield scrapy.Request('http://www.doumi.com'+link,callback=self.parse_item)
        self.page += 1
        print "loading page:" + str(self.page)
        if self.page<5:
            yield scrapy.Request("http://www.doumi.com/cd/o"+str(self.page)+"/",callback=self.parse)

    def parse_item(self,response):
        item=JianzhiItem()
        item['platform']="doumi"
        item['title']=response.xpath('//div[@class="main w clearfix"]/div[@class="jz-d-l"]/div[@class="jz-d-l-t clearfix"]/div[@class="jz-d-title"]/div/h2/text()').extract()
        item['money']=response.xpath('//div[@class="main w clearfix"]/div[@class="jz-d-l"]/div[@class="jz-d-l-t clearfix"]/div[@class="jz-d-title"]/div[@class="salary"]/span[@class="fl salary-num"]/text()').extract()[0]
        #
        item['content']=response.xpath('//div[@class="main w clearfix"]/div[@class="jz-d-l"]/div[@class="jz-d-l-b"]/div[@class="jz-d-info"]/div[@class="jz-d-area"]/p/text()').extract()+response.xpath('//div[@class="main w clearfix"]/div[@class="jz-d-l"]/div[@class="jz-d-l-b"]/div[@class="jz-d-info"]/p[@class="jz-d-area"]/text()').extract()
        #
        item['address'] = response.xpath('//div[@class="main w clearfix"]/div[@class="jz-d-l"]/div[@class="jz-d-l-b"]/div[@class="jz-d-info"]/div[@class="bg-work pr-80"]/div[@id="work-addr-open"]/div[@class="jz-d-area"]/text()').extract()

        item['detailUrl']=response.url
        yield item

    page+=1
    print "loading page:"+str(page)