"""
Created: 2/3/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from flask import jsonify, request, url_for

from budgeting.models import User
from budgeting.app.api.v1 import api_bp
from budgeting.app import db
from .errors import bad_request


@api_bp.route('/')
def home_page():
    return request.url_root


@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include username, email and password.')

    if User.query.filter_by(email=data['email']).first():
        return bad_request('Bad email. If this is your email address check your inbox.')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('apiv1.get_user', id=user.id)
    return response


@api_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
