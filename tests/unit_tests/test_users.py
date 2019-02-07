"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import pytest
from sqlalchemy.exc import IntegrityError

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

    def test_user_db_insert(self, db):
        """
        Verify that the user is being properly inserted into the db.
        :param db:
        :type db:
        :return:
        :rtype:
        """
        u = fake.ob_user()
        u1 = User(**u)
        assert u1.id is None
        db.session.add(u1)
        db.session.commit()
        assert isinstance(u1.id, int)

    def test_user_db_uniqueness(self, db):
        u = fake.ob_user()
        u1 = User(**u)
        db.session.add(u1)
        db.session.commit()

        u2 = User(**u)
        db.session.add(u2)

        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()
        db.session.commit()
