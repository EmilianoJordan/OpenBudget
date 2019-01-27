"""
Created: 1/26/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import g
from flask_httpauth import HTTPBasicAuth

from ....models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token: str = None, password: str = None):
    if not email_or_token:
        return False

    if not password:
        g.current_user = User.verify_auth_token(email_or_token)
        g.tokens_used = True
        return g.current_user is not None

    user = User.query.filter_by(email=email_or_token).first()

    if not user:
        return False

    g.current_user = user
    g.tokens_used = False
    return user.verify_password(password)