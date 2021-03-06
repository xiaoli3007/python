#coding=utf-8
from flask import render_template
from flask_mail import Message

from app import mail,app
from config import ADMINS

#装饰器
from app.common.decorators import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    if sender == '':
        sender = ADMINS[0]
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

#普通发送
'''
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
'''
#开启一个线程
'''
from threading import Thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
'''

def follower_notification(followed, follower):
    send_email("[microblog] %s is now following you!" % follower.nickname,
               ADMINS[0],
               [followed.email],
               render_template("member/follower_email.txt",
                               user = followed, follower = follower),
               render_template("member/follower_email.html",
                               user = followed, follower = follower))