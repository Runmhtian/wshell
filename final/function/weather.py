# coding=utf-8

from urllib import request
import json
import pickle
from bs4 import BeautifulSoup
from collections import namedtuple
import logging
from wshell.settings import BASE_DIR
import os
from final.static.city import CITY_DICT


logger=logging.getLogger(__name__)
staticpath=os.path.join(os.path.join(BASE_DIR,'final'),'static')


def query_weather(command,userid):
    # global CITY_DICT
    city=command.strip()
    if city=='':
        city='北京'
    # if not CITY_DICT:
    #     fp=open(os.path.join(staticpath,'city.pkl'),'rb')
    #     CITY_DICT=pickle.load(fp)
    #     fp.close()
    city_code=CITY_DICT.get(city)
    if city_code:
        '''
        查出来的不是最新的：
        weatherHtml = urllib2.urlopen('http://www.weather.com.cn/data/sk/%s.html'%city_code).read()
        weatherInfo=json.loads(weatherHtml).get('weatherinfo')
        for key,value in weatherInfo.items():
            print key,value
        '''
        ret=spider_weather(city_code)
        if ret:
            s=''
            for d_wea in ret:
                s+=u'【%s】%s,%s,%s\n'%(d_wea.day,d_wea.wea,d_wea.tem,d_wea.em)
            return s
        else:
            return 'an error has occurred!'
    else:
        return 'incorrect city,please check！'


def spider_weather(city_code):
    #  7天 url='http://www.weather.com.cn/weather/101011500.shtml'
    # 1天  http://www.weather.com.cn/weather1d/101011500.shtml

    weatherhtml = request.urlopen('http://www.weather.com.cn/weather/%s.shtml'%city_code).read()

    soup = BeautifulSoup(weatherhtml, 'html.parser')
    # # <input type="hidden" id="hidden_title" value="08月09日20时 周三  阴转多云  21/32°C">
    # realtime_info=soup.select('#hidden_title')[0].get('value')
    day_7=soup.select('#7d')[0].select('.clearfix')
    m = day_7[0].select('h1')
    n = day_7[0].select("p[class='wea']")
    x = day_7[0].select("p[class='tem']")
    y = day_7[0].select("p[class='win']")

    if len(m)!=len(n)!=len(x)!=len(y)!=7:
        logger.error('%s\n%s\n%s\n%s\n'%(m,n,x,y))
        return None

    d_wea = namedtuple('d_wea', ['day','wea', 'tem', 'em'])
    l=[]
    for i in range(7):
        # print m[i].string
        # print n[i].string
        # print ''.join([j for j in x[i].stripped_strings])
        # print y[i].select('i')[0].string
        d=m[i].string
        wea=n[i].string
        tem=''.join([j for j in x[i].stripped_strings])
        em=y[i].select('i')[0].string
        l.append(d_wea(day=d,wea=wea,tem=tem,em=em))
    return l



if __name__ == '__main__':
    pass