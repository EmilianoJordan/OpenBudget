"""
Created: 2/28/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
from . import api
from budgeting.models import User, Email

class EmailResource:
    pass


api.add_resource(EmailResource, '/user/<int:uid>/emails/', endpoint='email')
