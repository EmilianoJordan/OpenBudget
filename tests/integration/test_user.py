"""
Created: 2/7/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import json

from flask import url_for

from budgeting.models import User


class TestUser:

    def test_get_user_profile_page(self, client, user, get_auth_headers):
        """
        A user should be able to see their own user profile
        """
        u = User.query.filter_by(email=user['email']).one()
        r = client.get(
            url_for('api.get_user', id=u.id, _external=False),
            headers=get_auth_headers(user)
        )

        assert r.status_code == 200
        assert json.loads(r.get_data(as_text=True)) == u.to_dict()

    def test_other_user_profile_page(self, client, user_generator, get_auth_headers):
        """
        A user should not be able to see another user's profile page.
        """
        u1, u2 = user_generator(2)

        u = User.query.filter_by(email=u1['email']).one()

        r = client.get(
            url_for('api.get_user', id=u.id, _external=False),
            headers=get_auth_headers(u2)
        )

        assert r.status_code == 404

# @TODO this is not complete... need a lot more user testing.
