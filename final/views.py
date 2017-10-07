# coding=utf-8
from django.http import HttpResponse
import hashlib
import logging
from xml.etree import ElementTree
from .config import TOKEN
from django.shortcuts import render
import time
from .function import calulate,reminder,weather,ticket12306
from .utils import WELCOME,HELP

logger=logging.getLogger(__name__)
weather_pattern='(weather|wh)\s*(.*)'
reminder_pattern='(reminder|rd)\s*(\w)?\s*(.*)'
ticket_pattern='(ticket|tk)\s+(\S+)\s+(\S+)\s+(\d{8})\s*(.*)'


def analysis_text(text, userid):
    import re
    from .models import Last_command
    text = text.strip().lower()
    if text=='help':
        return HELP
    if text=='last' or text=='la':
        try:
            com=Last_command.objects.get(user_id=userid)
            return analysis_text(com.command,userid)
        except:
            return 'You probably havent used a command yet'
    com=Last_command(user_id=userid, command=text)
    com.save()
    if text.startswith('cal'):
        return calulate.cal(text)

    matched=re.match(weather_pattern,text)
    if matched:
        return weather.query_weather(matched.group(2),userid)

    matched = re.match(reminder_pattern, text)
    if matched:
        return reminder.deal_reminder(matched.group(2), matched.group(3),userid)
    matched=re.match(ticket_pattern,text)
    if matched:
        return ticket12306.query_ticket(
            matched.group(2),matched.group(3),matched.group(4),matched.group(5))
    else:
        return text


def weixin(request):
    if request.method=='GET':
        signature=request.GET.get('signature')
        timestamp=request.GET.get('timestamp')
        nonce=request.GET.get('nonce')
        echostr=request.GET.get('echostr')
        l=[TOKEN,timestamp,nonce]
        l.sort()
        s=''.join(l)
        sha1=hashlib.sha1()
        sha1.update(s.encode('utf-8'))
        if sha1.hexdigest() == signature:
            logger.info('认证成功')
            return HttpResponse(echostr)
        else:
            logger.debug('认证失败 %s'%request.GET)
            return HttpResponse('error')
    elif request.method=='POST':
        data=request.body
        xml=ElementTree.fromstring(data)
        msgtype = xml.find("MsgType").text
        userid = xml.find("FromUserName").text
        myid = xml.find("ToUserName").text
        if msgtype == "text":
            content = xml.find("Content").text
            ret_text=analysis_text(text=content,userid=userid)
            content={
                "toUser":userid,
                "fromUser":myid,
                "createTime":int(time.time()),
                "content":ret_text
            }
            return render(request,'reply_text.xml',content)
        elif msgtype == "event":
            event = xml.find("Event").text
            content = {
                "toUser": userid,
                "fromUser": myid,
                "createTime": int(time.time()),
                "content": WELCOME
            }
            if event == 'subscribe' or event == 'unsubscribe':
                return render(request,'reply_text.xml',content)
        else:
            return render(request,'reply_text.xml','an unsupported command')


def test(request):
    return HttpResponse('hello world %s'%time.ctime())

