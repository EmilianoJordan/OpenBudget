"""
Created: 1/21/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import os

from flask_migrate import Migrate

from budgeting.app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'base')
migrate = Migrate(app, db)
