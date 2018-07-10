# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LbscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 全国公共交易平台(四川)
class ScggjyItem(scrapy.Item):
    reportTitle = scrapy.Field()
    sysTime = scrapy.Field()
    url = scrapy.Field()
    entryName = scrapy.Field()
    entryOwner = scrapy.Field()
    ownerTel = scrapy.Field()
    tenderee = scrapy.Field()
    tendereeTel = scrapy.Field()
    biddingAgency = scrapy.Field()
    biddingAgencTel = scrapy.Field()
    placeAddress = scrapy.Field()
    placeTime = scrapy.Field()
    publicityPeriod = scrapy.Field()
    bigPrice = scrapy.Field()
    changeReason = scrapy.Field()
    oneTree = scrapy.Field()
    twoTree = scrapy.Field()
    threeTree = scrapy.Field()
    treeCount = scrapy.Field()
    oneCompany = scrapy.Field()
    onePrice = scrapy.Field()
    oneReviewPrice = scrapy.Field()
    oneScore = scrapy.Field()
    count = scrapy.Field()
