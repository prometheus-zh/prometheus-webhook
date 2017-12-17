# -*- coding:utf-8 -*-
from models import Email_Config, Email_Log
import smtplib
import email, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


def tomail(toemail_list, alert_content):
    smtpinfos = Email_Config.objects.all()[:1]
    for tosmtp in smtpinfos:
        username = tosmtp.smtp_user
        password = tosmtp.smtp_pass
        host = tosmtp.smtp_host
        port = tosmtp.smtp_port
        ssl = tosmtp.smtp_ssl
    # 收件人地址或是地址列表，支持多个收件人，最多30个
    # rcptto = ['***', '***']
    rcptto = ','.join(toemail_list)
    print(rcptto)
    # 构建alternative结构
    t1 = time.time()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header('告警邮件'.decode('utf-8')).encode()
    msg['From'] = '%s <%s>' % (Header('告警邮件'.decode('utf-8')).encode(), username)
    msg['To'] = rcptto
    t5 = time.time()
    # 这一步非常慢？
    msg['Message-id'] = email.utils.make_msgid()
    t2 = time.time()
    msg['Date'] = email.utils.formatdate()
    # 构建alternative的text/plain部分
    textplain = MIMEText(alert_content, _subtype='plain', _charset='UTF-8')

    msg.attach(textplain)


    # 构建alternative的text/html部分
    # texthtml = MIMEText('自定义HTML超文本部分', _subtype='html', _charset='UTF-8')
    # msg.attach(texthtml)
    # 发送邮件
    try:
        client = smtplib.SMTP()
        #python 2.7以上版本，若需要使用SSL，可以这样创建client
        if ssl == True:
            client = smtplib.SMTP_SSL()
        #SMTP普通端口为25或80
        client.connect(host, port)
        #开启DEBUG模式
        client.set_debuglevel(0)
        client.login(username, password)
        #发件人和认证地址必须一致
        #备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
        #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
        client.sendmail(username, rcptto, msg.as_string())
        client.quit()
        status = u'Mail sent successfully!'
    except smtplib.SMTPConnectError, e:
        status = u'The message failed to send and the connection failed:', e.smtp_code, e.smtp_error
    except smtplib.SMTPAuthenticationError, e:
        status = u'E-mail failed, authentication error:', e.smtp_code, e.smtp_error
    except smtplib.SMTPSenderRefused, e:
        status = u'The message was sent and the sender was rejected:', e.smtp_code, e.smtp_error
    except smtplib.SMTPRecipientsRefused, e:
        status = u'The message was sent and the recipient was rejected:', e.smtp_code, e.smtp_error
    except smtplib.SMTPDataError, e:
        status = u'E-mail failed to send, data received refused:', e.smtp_code, e.smtp_error
    except smtplib.SMTPException, e:
        status = u'E-mail failed to send, ', e.message
    except Exception, e:
        status = u'Mail sent exception, ', str(e)

    t3 = time.time()

    rs = Email_Log.objects.create(email=toemail_list, content=alert_content, status=status)
    rs.save()

    t4 = time.time()

    print('1:', t2-t1)
    print('0.5:', t5-t1)
    print('0.9:', t2-t5)

    print("2:", t3-t2)
    print('3:', t4-t3)

