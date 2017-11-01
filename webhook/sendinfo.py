# coding: utf-8
from models import CmsUser
from alertsendmail import *
from alertsms import *

def SendAlert(receiver,alert_content):
    toemail_list = list()
    tophone_list = list()
    send_list = CmsUser.objects.filter(group__name = receiver)
    for send_r in send_list:
        toemail_list.append(send_r.email.encode('utf8'))
        tophone_list.append(send_r.phone)
    try:
        tomail(toemail_list,alert_content)
    except:
        print 'send mail error'
    try:
        tosms(tophone_list,alert_content)
    except:
        print 'send sms error'


