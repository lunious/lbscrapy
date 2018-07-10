import redis
import json
import pymysql
from lbscrapy import settings
import logging

ITEM_KEY = 'sggjyzbjg:items'


def process_item(item):
    # 添加处理数据的代码
    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8',
        use_unicode=True
    )
    cursor = connect.cursor()

    if item['entryOwner'] != '':
        try:
            cursor.execute(
                "insert into sggjyzbjg (reportTitle,sysTime,url,entryName,entryOwner,ownerTel,tenderee,tendereeTel,biddingAgency,biddingAgencTel,placeAddress,placeTime,publicityPeriod,bigPrice,oneTree,twoTree,threeTree) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE entryName = entryName",
                (item['reportTitle'],
                 item['sysTime'],
                 item['url'],
                 item['entryName'],
                 item['entryOwner'],
                 item['ownerTel'],
                 item['tenderee'],
                 item['tendereeTel'],
                 item['biddingAgency'],
                 item['biddingAgencTel'],
                 item['placeAddress'],
                 item['placeTime'],
                 item['publicityPeriod'],
                 item['bigPrice'],
                 item['oneTree'],
                 item['twoTree'],
                 item['threeTree'],
                 ))
            connect.commit()
        except Exception as error:
            logging.log(error)
        try:
            cursor.execute(
                "Insert into entryjglist(entryName,sysTime,type,entity,entityId) select reportTitle,sysTime,'工程中标结果','sggjyzbjg',id from sggjyzbjg where id not in(select entityId from entryjglist where  entity ='sggjyzbjg' ) ")
            connect.commit()
            print('数据插入成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        except Exception as error:
            logging.log(error)
            print('数据插入失败>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')


def main():
    r = redis.StrictRedis(host='120.78.161.254', port=6379)
    for _ in range(r.llen(ITEM_KEY)):
        data = r.lpop(ITEM_KEY)
        item = json.loads(data.decode('utf8'))
        process_item(item)


if __name__ == '__main__':
    main()
