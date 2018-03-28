# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianzhiItem(scrapy.Item):
    # define the fields for your item here like:
    #
    # biaoti: //div[@class="left"]/div[@class="items"]/div[@class="item clearfix"]/div[@class="item1"]/h2
    # money : //div[@class="left"]/div[@class="items"]/div[@class="item clearfix"]/div[@class="item2"]/div/span
    # detailUrl: //div[@class="left"]/div[@class="items"]/div[@class="item clearfix"]/div[@class="item1"]/h2/a/@href
    itemNo=scrapy.Field()
    title = scrapy.Field()
    money = scrapy.Field()
    content= scrapy.Field()
    address=scrapy.Field()
    platform=scrapy.Field()
    detailUrl = scrapy.Field()
