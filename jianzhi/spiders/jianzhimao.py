# -*- coding: utf-8 -*-

# 兼职猫兼职 spider
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianzhi.items import JianzhiItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
class jianzhimao(CrawlSpider):
    name = 'jianzhimao'
    allowed_domains = ['chengdu.jianzhimao.com']
    page=1

    url="http://chengdu.jianzhimao.com/pixian_zbx_0/index"+str(page)+".html"
    start_urls = [url]


    def deal_span(self,text):
        soup = BeautifulSoup(text)
        text=soup.span.get_text()
        a=""
        if soup.a:
            a=soup.a.get_text()
        return text+a

    def parse(self,response):
        links=response.xpath('//section[@class="container"]/article[@class="w_main"]/div[@class="content_box clearfix"]/div[@class="content_list_box"]/ul[@class="content_list_wrap"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request('http://chengdu.jianzhimao.com'+link,callback=self.parse_item)
        self.page += 1
        print "loading page:" + str(self.page)
        if self.page<5:
            yield scrapy.Request("http://chengdu.jianzhimao.com/pixian_zbx_0/index"+str(self.page)+".html",callback=self.parse)

    def parse_item(self,response):
        item=JianzhiItem()
        item['platform']="jianzhimao"
        item['title']=response.xpath('//section[@class="container"]/article[@class="w_main"]/div[@class="content_box clearfix"]/div[@class="p_left"]/div[@class="content_wrap"]/div[@class="job_header"]/h1/text()').extract()
        item['money']=response.xpath('//section[@class="container"]/article[@class="w_main"]/div[@class="content_box clearfix"]/div[@class="p_left"]/div[@class="content_wrap"]/div[@class="job_header"]/div[@class="job_base"]/span[@class="job_price"]/text()').extract()[0]
        #
        item['content']=response.xpath('//section[@class="container"]/article[@class="w_main"]/div[@class="content_box clearfix"]/div[@class="p_left"]/div[@class="content_wrap"]/div[@class="job_content"]/div[@class="box"]/div[@class="detail"]/text()').extract()
        #
        item['address'] = response.xpath('//section[@class="container"]/article[@class="w_main"]/div[@class="content_box clearfix"]/div[@class="p_left"]/div[@class="content_wrap"]/div[@class="job_content"]/ul[@class="job_list"]/li/span[@class="con"]/text()').extract()[2]

        item['detailUrl']=response.url
        yield item

    page+=1
    print "loading page:"+str(page)