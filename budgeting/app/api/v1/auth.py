from flask import g, url_for, jsonify, request
from flask_httpauth import HTTPBasicAuth

from budgeting.models import User

from . import api_bp
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token: str = None, password: str = None):
    if not email_or_token:
        if url_for('api.user_post') == request.url_rule.rule and 'POST' == request.method:
            return True
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


@api_bp.route('/tokens', methods=['POST'])
def get_token():
    if g.token_used:
        return unauthorized('Invalid Credentials')
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=3600),
        'expiration': 3600
    })


@api_bp.before_request
@auth.login_required
def before_request():
    if url_for('api.user_post') == request.url_rule.rule and 'POST' == request.method:
        return

    if url_for('api.user_verify') == request.url_rule.rule and 'GET' == request.method:
        return

    if not g.current_user.confirmed:
        return forbidden('Unconfirmed account')
