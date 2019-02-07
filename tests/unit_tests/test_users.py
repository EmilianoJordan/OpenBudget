"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import pytest

from budgeting.models import User

from tests.helpers import fake


class TestUserModel:

    def test_user_initialization(self):
        u = fake.ob_user()
        u1 = User(**u)

        assert u1.email == u['email']
        assert u1.username == u['username']
        assert u1.password_hash != u['password']

        with pytest.raises(AttributeError):
            u1.password

        assert u1.verify_password(u['password'])

    def test_user_db(self, db):
        u = fake.ob_user()
        u1 = User(**u)
        db.session.add(u1)
        db.session.commit()
        print(u1.id)