# coding=utf-8

import requests
import os
import threading
import json
import logging
import time
import random
import urllib
from final.utils import retry


static_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static')
logger=logging.getLogger(__name__)
stations=dict()
seat_dict={
    '高软':21,
    '软卧':23,
    '软座':24,
    '无座':26,
    '硬卧':28,
    '硬座':29,
    '二等座': 30,
    '一等座': 31,
    '商务座': 32,
    '动卧': 33
}

class Ticket:
    def __init__(self,args):
        self.train_code=args[3]
        self.start_station_name =args[4]
        self.end_station_name =args[5]
        self.from_station_name = args[6]
        self.to_station_name = args[7]
        self.start_time = args[8]
        self.arrive_time = args[9]
        self.duration=args[10]
        self.start_train_date = args[13]

        self.seats={
        '高软': args[21],
        '软卧': args[23],
        '软座': args[24],
        '无座': args[26],
        '硬卧': args[28],
        '硬座': args[29],
        '二等座':args[30],
        '一等座': args[31],
        '商务座': args[32],
        '动卧': args[33]
        }

    def __str__(self):
        s='【%s】%s-%s'%(self.train_code,self.start_time,self.arrive_time)
        for key,value in self.seats.items():
            if value not in ['','无']:
                s+='[%s:%s]'%(key,value)
        return s

    __rper__=__str__

    def get_str(self,seats):
        s = '【%s】%s-%s' % (self.train_code, self.start_time, self.arrive_time)
        for key, value in self.seats.items():
            if key in seats:
                if value not in ['', '无']:
                    s += '[%s:%s]' % (key, value)
        return s


def station_info():

    station_url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    station_path=os.path.join(static_path,'station_name.js')
    if not os.path.exists(station_path):
        logger.info('正在下载站点信息文件...')
        s=requests.session()
        resp=s.get(station_url, timeout=5, verify=False)
        assert resp.status_code==200
        with open(station_path,'wb') as f:
            f.write(resp.content)
    with open(station_path,'r',encoding='utf-8') as f:
        data=f.read()
        station_list=data.split('@')[1:]
        for station in station_list:
            items=station.split('|')
            stations[items[1]]=items[2]


class Order(threading.Thread):
    def __init__(self,train_date,from_station,to_station,seats=None):
        super(Order, self).__init__(name='thread')
        self.train_date=train_date
        self.from_station=stations.get(from_station)
        self.to_station=stations.get(to_station)
        self.from_station_name=from_station
        self.to_station_name=to_station
        self.s=requests.session()
        self.s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                            '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                               })
        self.tickets=[]
        if seats:
            self.seats=seats
        else:
            self.seats=seat_dict.keys()
        self.purpose_code = 'ADULT'

    def _check_tickets(self,ticket):
        if ticket[11]!='Y':
            return False
        else:
            for seat in self.seats:
                if ticket[seat_dict[seat]] not in ['无','']:
                    return True
        return False

    @retry(3)
    def _query_ticket(self):
        url_init='https://kyfw.12306.cn/otn/leftTicket/init'
        resp = self.s.get(url_init,verify=False)
        if resp.status_code!=200:
            return False
        cookies=resp.cookies

        cookies_t1=str(self.from_station_name.encode('unicode_escape').replace(b'\\',b'%'))[2:-1]+'%2C'+self.from_station
        cookies_t2 = str(self.to_station_name.encode('unicode_escape').replace(b'\\', b'%'))[
                     2:-1] + '%2C' + self.to_station

        cookies.set('_jc_save_fromStation', cookies_t1, domain='kyfw.12306.cn',
                    path='/')
        cookies.set('_jc_save_toStation', cookies_t2, domain='kyfw.12306.cn',
                    path='/')
        cookies.set('_jc_save_fromDate', self.train_date, domain='kyfw.12306.cn', path='/')
        cookies.set('_jc_save_toDate', self.train_date, domain='kyfw.12306.cn', path='/')
        cookies.set('_jc_save_wfdc_flag', 'dc', domain='kyfw.12306.cn', path='/')

        url_query=r'https://kyfw.12306.cn/otn/leftTicket/queryX'

        parameters=[
        ('leftTicketDTO.train_date',self.train_date),
        ('leftTicketDTO.from_station',self.from_station),
        ('leftTicketDTO.to_station',self.to_station),
        ('purpose_codes',self.purpose_code)
        ]
        resp=self.s.get(url_query,cookies=cookies,params=parameters,verify=False,timeout=10,allow_redirects=True)
        # print(resp.url)
        if resp.status_code==200:
            js=resp.json()
            data=js.get('data').get('result')
            if len(data) == 0:
                return
            for result in data:
                infos = result.strip().split('|')
                if self._check_tickets(infos):
                    self.tickets.append(Ticket(infos))
            if len(self.tickets)==0:
                return '没有满足要求的车次'
            else:
                return '\n'.join([ticket.get_str(self.seats) for ticket in self.tickets])
        else:
            return

    def run(self):
        self.ret_message=self._query_ticket()



def query_ticket(from_station,to_station,train_date,seats=None):
    #参数检测
    if len(stations) == 0:
        station_info()
    order = Order(train_date, from_station, to_station, seats=seats)
    order.start()
    order.join()
    return order.ret_message


if __name__ == '__main__':
    if len(stations)==0:
        station_info()
    train_date='2017-09-27'
    from_station=u'北京'
    to_station=u'上海'
    seats=[u'二等座',u'一等座',u'硬座']
    order=Order(train_date,from_station,to_station,seats=seats)
    order.start()
