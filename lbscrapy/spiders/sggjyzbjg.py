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
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[2]/text()').extract():
            one = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[2]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td/text()').extract():
            one = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td/text()').extract()
        else:
            one = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[3]/text()').extract():
            one_1 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[3]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[2]/text()').extract():
            one_1 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[2]/text()').extract()
        else:
            one_1 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[4]/text()').extract():
            one_2 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[4]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[3]/text()').extract():
            one_2 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[3]/text()').extract()
        else:
            one_2 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[5]/text()').extract():
            one_3 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/td[5]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[4]/text()').extract():
            one_3 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[2]/th[4]/text()').extract()
        else:
            one_3 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[2]/text()').extract():
            two = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[2]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td/text()').extract():
            two = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td/text()').extract()
        else:
            two = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[3]/text()').extract():
            two_1 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[3]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[2]/text()').extract():
            two_1 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[2]/text()').extract()
        else:
            two_1 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract():
            two_2 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/td[4]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[3]/text()').extract():
            two_2 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[3]/th[3]/text()').extract()
        else:
            two_2 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[3]/td[4]/text()').extract():
            two_3 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[3]/td[4]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[3]/th[4]/text()').extract():
            two_3 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[3]/th[4]/text()').extract()
        else:
            two_3 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[2]/text()').extract():
            three = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[2]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td/text()').extract():
            three = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td/text()').extract()
        else:
            three = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[3]/text()').extract():
            three_1 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[3]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[2]/text()').extract():
            three_1 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[2]/text()').extract()
        else:
            three_1 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[4]/td[4]/text()').extract():
            three_2 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[4]/td[4]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[4]/th[3]/text()').extract():
            three_2 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]/tr[4]/th[3]/text()').extract()
        else:
            three_2 = '/'
        if Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[5]/text()').extract():
            three_3 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/td[5]/text()').extract()
        elif Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[4]/text()').extract():
            three_3 = Selector(text=res[0]).xpath('//div[@class="tablediv"]/table[2]//tr[4]/th[4]/text()').extract()
        else:
            three_3 = '/'
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
        if one:
            item['oneTree'] = one[0] + '_' + one_1[0] + '_' + one_2[0] + '_' + one_3[0]
        else:
            item['oneTree'] = ''
        if two:
            item['twoTree'] = two[0] + '_' + two_1[0] + '_' + two_2[0] + '_' + two_3[0]
        else:
            item['twoTree'] = ''
        if three:
            item['threeTree'] = three[0] + '_' + three_1[0] + '_' + three_2[0] + '_' + three_3[0]
        else:
            item['threeTree'] = ''
        yield item
