# coding: utf-8
from yunpian.SmsOperator import SmsOperator
import sys
import json
from models import Sms_Log,Sms_Config
reload(sys)
sys.setdefaultencoding('utf-8')

def tosms(tosms_lists,alert_content):
    print alert_content
    APIKEY = None
    smsinfos = Sms_Config.objects.all()[:1]
    for smsinfo in smsinfos:
        APIKEY = smsinfo.api_key
    if APIKEY == None:
        rs = Sms_Log.objects.create(phone=tosms_lists,content=alert_content,status='没有配置APIKEY所以无法发送')
        rs.save()
        exit(1)

    smsOperator = SmsOperator(APIKEY)
    #这个是个性化接口发送，批量发送的接口耗时比单号码发送长，
    #如果需要更高并发速度，推荐使用single_send/tpl_single_send
    status = list()
    for tosms_list in tosms_lists:
        status.append(json.dumps(smsOperator.multi_send(\
        {'mobile': tosms_list, 'text': '【监控告警】故障告警:'+alert_content}).content,ensure_ascii=False))

    rs = Sms_Log.objects.create(phone=tosms_lists,content=alert_content,status=status)
    rs.save()


