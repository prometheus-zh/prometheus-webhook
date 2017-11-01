# coding: utf-8
from models import Allow_Ip
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from webhook.sendinfo import SendAlert

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def sendmessage(request):
    '''
      post {"receiver":"receiver_name",\
      alerts:{"annotations":"description":"game over","annotations": {"description":"game over"}}

      '''
    remote_addr = request.META['REMOTE_ADDR']
    if remote_addr:
        rs = get_object_or_404(Allow_Ip,ip=remote_addr)
        if rs:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            receiver = body['receiver']
            for alert in body['alerts']:
                alert_content = str(alert['annotations']['description'])
                SendAlert(receiver,alert_content)

    return HttpResponse("ok")

@csrf_exempt
def index(request):
    return HttpResponseRedirect('/admin')