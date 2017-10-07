# coding=utf-8

from final.models import Reminder

'''
备忘录

reminder l  显示备忘目录
reminder 显示最近一条备忘
reminder c str  创建一条备忘
reminder i id  显示指定备忘
reminder r id 删除


vald_falg  是否可用
id user_id reminder date
'''

REMINDER_HELP="""【备忘功能】|
reminder/rd 显示最近一条备忘|
reminder/rd c info 创建备忘|
reminder/rd l 显示备忘id列表|
reminder/rd i id 显示id详细信息|
reminder/rd r id 删除此id|
reminder/rd h 显示帮助
"""


def deal_reminder(flag,desc,userid):
    if flag=='c':
        if desc=='':
            return 'create reminder failed,please use [rd c info]'
        rem=Reminder(user_id=userid,reminder=desc,vald_flag=True)
        rem.save()
        return 'use [reminder i %d] display'%rem.id
    elif flag=='i':
        if desc=='':
            return 'please use [rd i id]'
        try:
            rem=Reminder.objects.get(id=int(desc),vald_flag=True)
            return u'【%s】%s'%(rem.date,rem.reminder)
        except:
            return 'id not found,please check id'
    elif flag=='l':
        rems=Reminder.objects.filter(user_id=userid,vald_flag=True).order_by('-date')[0:10]
        if len(rems)!=0:
            l=[]
            for rem in rems:
                s='%d %s'%(rem.id,rem.date)
                l.append(s)
            return '\n'.join(l)
        else:
            return 'You probably dont have a reminder'
    elif not flag and desc=='':
        rem = Reminder.objects.filter(user_id=userid, vald_flag=True).order_by('-id')[0]
        if len(rem)!=0:
                return u'【%s】%s' % (rem.date, rem.reminder)
        else:
            return 'You probably dont have a reminder'
    elif flag=='r':
        try:
            rem=Reminder.objects.get(id=int(desc))
            rem.vald_flag=False
            rem.save()
        except:
            return 'id not found,please check id'
    elif flag=='h':
        return REMINDER_HELP
    else:
        return '无此命令'