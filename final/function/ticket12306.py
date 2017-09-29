# coding=utf-8

import requests
import os
import threading
import json
import logging
import time
import random
import urllib
from final.utils import retry,str2date
from final.static.stations import station_dict


logger=logging.getLogger(__name__)
session=None
create_time=0

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

headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                            '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
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


class Order():
    def __init__(self,train_date,from_station,to_station,seats=None,session=None):
        self.train_date=train_date
        self.from_station=station_dict.get(from_station)
        self.to_station=station_dict.get(to_station)
        self.from_station_name=from_station
        self.to_station_name=to_station
        self.tickets=[]
        if seats:
            self.seats=seats
        else:
            self.seats=seat_dict.keys()
        self.purpose_code = 'ADULT'
        self.ret_message=''
        self.session=session

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

        cookies=self.session.cookies
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
        # print(cookies)
        url_query=r'https://kyfw.12306.cn/otn/leftTicket/queryX'

        parameters=[
        ('leftTicketDTO.train_date',self.train_date),
        ('leftTicketDTO.from_station',self.from_station),
        ('leftTicketDTO.to_station',self.to_station),
        ('purpose_codes',self.purpose_code)
        ]
        resp=self.session.get(url_query,cookies=cookies,params=parameters,verify=False,timeout=10,allow_redirects=True)
        print(resp.url)
        if resp.status_code==200 and resp.json():
            js=resp.json()
            if 'data' not in js.keys():
                print('2')
                return False
            print(js)
            data=js.get('data').get('result')
            if len(data) == 0:
                print('3')
                return False
            for result in data:
                infos = result.strip().split('|')
                if self._check_tickets(infos):
                    self.tickets.append(Ticket(infos))
            if len(self.tickets)==0:
                self.ret_message='没有满足要求的车次'
                return True
            else:
                self.ret_message='\n'.join([ticket.get_str(self.seats) for ticket in self.tickets])
                return True
        else:
            print('4')
            return False

    def run(self):
        self._query_ticket()

@retry(3)
def update_session():
    global session
    url_init = 'https://kyfw.12306.cn/otn/leftTicket/init'
    session = requests.Session()
    session.headers.update(headers)
    resp = session.get(url_init, verify=False)
    if resp.status_code==200:
        return True
    else:
        return False

def query_ticket(from_station,to_station,train_date,seats=None):
    import time
    global create_time
    if from_station not in station_dict.keys() or to_station not in station_dict.keys():
        return '请确认输入城市名称是否正确'
    import datetime

    if (str2date(train_date)-datetime.datetime.now().date()).days>30:
        return '预售期为30天'
    train_date = str2date(train_date).strftime('%Y-%m-%d')
    if seats or seats!='':
        seats=seats.replace('，',',')
        if ',' in seats:
            seats=seats.split(',')
            for seat in seats:
                if seat not in seat_dict.keys():
                    return '请输入正确的坐席'
        else:
            if seats not in seat_dict.keys():
                return '请输入正确的坐席'
            else:
                seats=[seats]

    if time.time()-create_time>3600.0:
        update_session()

    order = Order(train_date, from_station, to_station, seats=seats,session=session)
    order.run()
    return order.ret_message





if __name__ == '__main__':
    train_date='20171010'
    from_station=u'北京'
    to_station=u'天津'
    seats='硬座,一等座'
    print(query_ticket(from_station,to_station,train_date,seats))
