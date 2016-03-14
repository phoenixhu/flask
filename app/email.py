#coding=utf-8
from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


# 异步发送邮件函数
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# 发送邮件函数
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    '''发送邮件函数，参数分别为：收件人地址，主题，渲染邮件正文的模板，关键字参数列表'''
    # 定义一封邮件，参数分别为主题，发件人，收件人
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # 渲染纯文本正文
    msg.body = render_template(template + '.txt', **kwargs)
    # 渲染富文本正文
    msg.html = render_template(template + '.html', **kwargs)
    # 异步发送邮件
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr