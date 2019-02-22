"""
Created: 2/20/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from ..app import db


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email
