"""
Created: 2/15/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import os

from flask_mail import Message

from . import mail, create_app
from .decorators import thread

@thread
def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body, sender=None):
    if sender:
        msg = Message(subject, sender=sender, recipients=recipients)
    else:
        msg = Message(subject, recipients=recipients)

    msg.body = text_body
    msg.html = html_body
    _send_async_email(create_app(), msg)
