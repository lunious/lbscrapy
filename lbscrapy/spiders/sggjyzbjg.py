# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import datetime
import json
import time
from lbscrapy.items import ScggjyItem
from scrapy.selector import Selector


class SggjyzbjgSpider(RedisSpider):
    name = 'sggjyzbjg'
    allowed_domains = ['scggzy.gov.cn']
    # start_urls = ['http://scggzy.gov.cn/']
    page = 1
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 转换成时间数组
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    url = 'http://www.scggzy.gov.cn/Info/GetInfoListNew?keywords=&times=5&timesStart=&timesEnd=&province=&area=&businessType=project&informationType=TenderCandidateAnnounce&industryType='

    def parse(self, response):
        if response.status == 200:
            yield scrapy.Request(url=self.url + '&page=' + str(self.page) + '&parm=' + str(self.timestamp),
                                 callback=self.list_parse)

    def list_parse(self, response):
        js = json.loads(response.body_as_unicode())
        if '成功' == js['message']:
            data = json.loads(js['data'])
            pageCount = js['pageCount']
            items = []
            for each in data:
                item = ScggjyItem()
                item['reportTitle'] = each['Title']
                item['sysTime'] = each['CreateDateStr']
                item['url'] = 'http://www.scggzy.gov.cn' + each['Link']
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.detail_parse)

            if self.page < pageCount:
                self.page += 1

            yield scrapy.Request(url=self.url + '&page=' + str(self.page) + '&parm=' + str(self.timestamp),
                                 callback=self.list_parse)

    def detail_parse(self, response):
        item = response.meta['meta']
        res = response.xpath('//*[@id="hidSeven0"]/@value').extract()
        entryName = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[1]/td[2]/text()').extract()
        entryOwner = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[2]/td[2]/text()').extract()
        ownerTel = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[2]/td[4]/text()').extract()
        tenderee = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[3]/td[2]/text()').extract()
        tendereeTel = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[3]/td[4]/text()').extract()
        biddingAgency = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[4]/td[2]/text()').extract()
        biddingAgencTel = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[4]/td[4]/text()').extract()
        placeAddress = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[5]/td[2]/text()').extract()
        placeTime = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[5]/td[4]/text()').extract()
        publicityPeriod = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[6]/td[2]/text()').extract()
        bigPrice = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[1]//tr[6]/td[4]/text()').extract()

        oneTree = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[2]//text()')
        content1 = ''
        for i in oneTree.extract():
            content1 += i.strip() + '_'
        if content1.startswith('_'):
            item['oneTree'] = content1[6:-2].replace('__','_')
        else:
            item['oneTree'] = content1[4:-2]
        twoTree = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[3]//text()')
        content2 = ''
        for i in twoTree.extract():
            content2 += i.strip() + '_'
        if content2.startswith('_'):
            item['twoTree'] = content1[6:-2].replace('__', '_')
        else:
            item['twoTree'] = content2[4:-2]
        threeTree = Selector(text=res[0].strip()).xpath('//div[@class="tablediv"]/table[2]//tr[4]//text()')
        content3 = ''
        for i in threeTree.extract():
            content3 += i.strip() + '_'
        if content3.startswith('_'):
            item['threeTree'] = content1[6:-2].replace('__', '_')
        else:
            item['threeTree'] = content2[4:-2]

        if entryName:
            item['entryName'] = entryName[0]
        else:
            item['entryName'] = ''
        if entryOwner:
            item['entryOwner'] = entryOwner[0]
        else:
            item['entryOwner'] = ''
        if ownerTel:
            item['ownerTel'] = ownerTel[0]
        else:
            item['ownerTel'] = ''
        if tenderee:
            item['tenderee'] = tenderee[0]
        else:
            item['tenderee'] = ''
        if tendereeTel:
            item['tendereeTel'] = tendereeTel[0]
        else:
            item['tendereeTel'] = ''
        if biddingAgency:
            item['biddingAgency'] = biddingAgency[0]
        else:
            item['biddingAgency'] = ''
        if biddingAgencTel:
            item['biddingAgencTel'] = biddingAgencTel[0]
        else:
            item['biddingAgencTel'] = ''
        if placeAddress:
            item['placeAddress'] = placeAddress[0]
        else:
            item['placeAddress'] = ''
        if placeTime:
            item['placeTime'] = placeTime[0]
        else:
            item['placeTime'] = ''
        if publicityPeriod:
            item['publicityPeriod'] = publicityPeriod[0]
        else:
            item['publicityPeriod'] = ''
        if bigPrice:
            item['bigPrice'] = bigPrice[0]
        else:
            item['bigPrice'] = ''

        if item['oneTree'] or item['twoTree'] or item['threeTree']:
            item['treeCount'] = 3
        else:
            item['treeCount'] = 0
        yield item
