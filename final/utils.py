# coding=utf-8
import sys
import os
import logging

logger=logging.getLogger(__name__)
base_dir=os.path.dirname(os.path.dirname(__file__))

WELCOME="欢迎关注me！"

'''
MENU = {
    "button": [
        {
            "type": "click",
            "name": "使用帮助",
            "key": 'V1'
        },
        {
            "type": "click",
            "name": "关于我",
            "key": "V2"
        }]
}

'''



# access_token = "I6-cIxDex7duOdC2guHhDWQftd9doaFw6GOo_JoSj3EOqvtZ5MOUqbgwWzglNL-yPZvzf3RKVqFpDQz9d9q0L1Tn" \
#                "OoHJCWAQa4jKk27HSRsYXFaAGAFEM"
# errcode_token = [42001, 41001, 40014]



def retry(arg):
    def _retry(func):
        def __retry(*args,**kwargs):
            for i in range(arg):
                ret=func(*args,**kwargs)
                if ret:
                    return ret
            return '查询失败'
        return __retry
    return _retry



if __name__ == '__main__':
    test()
















# def update_token():
#     global access_token
#     url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(APPID,APPSECRET)
#     response=request.urlopen(request.Request(url))
#     content=response.read()
#     info=json.loads(content)   # 从json格式的字符串转化为python数据类型
#     if "errcode" in info.keys():
#         logger.error(KeyError('更新token出错：%s'%info.get("errcode")))
#     access_token=info.get('access_token')
#
#
# def update_menu():
#     url="https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"%access_token
#     req=request.Request(url,data=urlencode(MENU),
#                         headers={'Content-Type':'application/json','encoding':'utf-8'})
#     response=request.urlopen(req)  # 从python数据类型转换为json类型的字符串
#     info = json.loads(response.read())
#     errcode=info.get('errcode')
#     if errcode==0:
#         logger.info('更新菜单成功')
#     elif errcode in errcode_token:
#         update_token()
#         update_menu()
#     else:
#         raise RuntimeError('更新菜单出错：%d'%errcode)
#
#
# def get_user_info(userid):
#     url='https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN'%(access_token,userid)
#     response=request.urlopen(url)
#     info=json.loads(response.read())
#     if 'errcode' in info.keys():
#         errcode=info.get('errcode')
#         if errcode in errcode_token:
#             update_token()
#             return get_user_info(userid)
#         else:
#             raise RuntimeError('获取用户信息出错：%d' % errcode)
#     else:
#         subscribe=info.get('subscribe')
#         nickname=info.get('nickname')
#         if subscribe==1:
#             return nickname
#         else:
#             raise NameError('非关注用户或者id非法')
#
#
# def get_mutiluser_info(userid_list):
#     url='https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s'%access_token
#     dic_json={
#         "user_list":[]
#     }
#     for userid in userid_list:
#         dic_json['user_list'].append({'openid':userid, "lang": "zh-CN"})
#
#     req=request.Request(url,data=urlencode(dic_json)
#                         ,headers={'Content-Type':'application/json','encoding':'utf-8'})
#     response=request.urlopen(req)
#     info=json.loads(response.read())
#     if 'errcode' in info.keys():
#         errcode = info.get('errcode')
#         if errcode in errcode_token:
#             update_token()
#             return get_mutiluser_info(userid_list)
#         else:
#             raise RuntimeError('获取用户列表信息出错：%d' % errcode)
#     else:
#         name_list=[]
#         for user in info.get('user_info_list'):
#             if user.get('subscribe')==1:
#                 # openid=user.get('openid')
#                 nickname= user.get('nickname')
#                 name_list.append(nickname)
#         return name_list
#
#
# def get_openid(code):
#     url='https://api.weixin.qq.com/sns/oauth2/access_token?' \
#         'appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID,APPSECRET,code)
#     response=request.urlopen(url)
#     info=json.loads(response.read())
#     return info.get('openid')
#
#
# if __name__ == '__main__':
#     print(get_mutiluser_info(['o6ngQv5DAxoOoABubGsPCYLynFFc','o6ngQv2BwJipHSaHN8_m-RTTT3nw']))