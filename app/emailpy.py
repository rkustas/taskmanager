from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    Thread(target=send_async_email, 
        args=(current_app._get_current_object(),msg)).start()

def task_update(user):
    send_email('New Task Posted!',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/update_task.txt',
                                         user=user),
               html_body=render_template('email/update_task.html',
                                         user=user))

def pastdue_email(task):
    send_email('Task Past Due!',
               sender=current_app.config['ADMINS'][0],
               recipients=[task.user.email],
               text_body=render_template('email/past_due.txt',
                                         task=task),
               html_body=render_template('email/past_due.html',
                                         task=task))


