# coding:utf8
from models import Wechat_Config, Wechat_Log
import requests
import json, time

def get_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {
        'corpid': Wechat_Config.objects.get(pk=1).wechat_id,
        'corpsecret': Wechat_Config.objects.get(pk=1).wechat_key,
       }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]


def wechat_msg(w_id, level="xx", details="yy"):
    url = ("https://qyapi.weixin.qq.com/cgi-bin/message/send"
          "?access_token={}").format(get_token())
    if level == "fatal":
        style = 'highlight'
    else:
        style = 'normal'
        '''
        description" : "<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">
        恭喜你抽中iPhone 7一台，领奖码：xxxx</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>"'''
    status = list()
    for i in w_id:
        values = {
           "touser": i,
           "msgtype": "text",
           "agentid": Wechat_Config.objects.get(pk=1).wechat_agent_id,
           #  'title': u"标题: Prometheus警报信息",
           "text": {
               "content": u"标题: Prometheus警报信息 \n\n等级：%s \n\n详情: %s" % (level, details)
           }
           #  "description": "<div class=\"gray\">%s</div>"
           # " <div class=%s>%s</div>" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), style, details),
           #  'url': 'http://www.baidu.com'
           }
        print('sed``````````````````')
        status.append(requests.post(url, json.dumps(values)).status_code)
        print('sed``````````````````')
    rs = Wechat_Log.objects.create(wechat=w_id, content=details, status=status)
    rs.save()



