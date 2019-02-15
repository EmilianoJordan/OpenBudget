"""
Created: 2/7/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import json

from bs4 import BeautifulSoup
from flask import url_for
import pytest


from budgeting.app import mail
from budgeting.models import User
from budgeting.models.permissions import BasicUserRoles

from tests.helpers import fake


@pytest.mark.user
class TestUser:

    def test_get_user_profile_page(self, client, user, get_auth_headers):
        """
        A user should be able to see their own user profile
        """
        u = User.query.filter_by(email=user['email']).one()
        r = client.get(
            url_for('api.user', u_id=u.id, _external=False),
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
            url_for('api.user', u_id=u.id, _external=False),
            headers=get_auth_headers(u2)
        )

        assert r.status_code == 404

    def test_user_list_as_admin(self, client, employee_admin, user_generator, get_auth_headers):
        """
        Verify that an admin or employee has rights to view the user
        list.
        """
        r = client.get(
            url_for('api.user_list', page=1, _external=False),
            headers=get_auth_headers(employee_admin),
        )

        assert r.status_code == 200

        assert r.json['page'] == 1
        assert r.json['per_page'] == 20
        assert r.json['count'] == User.query.count()
        for user in r.json['users']:
            assert User.query.filter_by(username=user['username']).count() == 1

    def test_user_list_as_admin_no_page(self, client, employee_admin,
                                        user_generator, get_auth_headers):
        """
        Verify that if no page is passed to the endpoint the page
        returned is page 1.
        """
        r = client.get(
            url_for('api.user_post', _external=False),
            headers=get_auth_headers(employee_admin),
        )

        assert r.status_code == 200

        assert r.json['page'] == 1
        assert r.json['per_page'] == 20
        assert r.json['count'] == User.query.count()
        for user in r.json['users']:
            assert User.query.filter_by(username=user['username']).count() == 1

    @pytest.mark.long
    def test_user_list_multi_page(self, client, employee_admin,
                                  user_generator, get_auth_headers):
        """
        Verify pagination of the user list page.
        """
        users = user_generator(41)
        headers = get_auth_headers(employee_admin)

        r = client.get(
            url_for('api.user_post', _external=False),
            headers=headers,
        )

        assert r.status_code == 200

        assert r.json['page'] == 1
        assert r.json['per_page'] == 20
        assert r.json['count'] == User.query.count()
        assert r.json['prev'] == ''
        assert r.json['next'] == url_for('api.user_list', page=2)

        r = client.get(
            r.json['next'],
            headers=headers,
        )

        assert r.json['page'] == 2
        assert r.json['per_page'] == 20
        assert r.json['count'] == User.query.count()
        assert r.json['prev'] == url_for('api.user_list', page=1)
        assert r.json['next'] == url_for('api.user_list', page=3)

        r = client.get(
            r.json['next'],
            headers=headers,
        )
        assert r.json['page'] == 3
        assert r.json['per_page'] == 20
        assert r.json['count'] == User.query.count()
        assert r.json['prev'] == url_for('api.user_list', page=2)
        assert r.json['next'] == ''

        r = client.get(
            r.json['prev'],
            headers=headers,
        )
        assert r.status_code == 200

    def test_user_list_as_user(self, client, user, get_auth_headers):
        """
        Verify that you need admin access to view the user list. No
        user should be able to view the list.

        Verify that user list returns a not found error to protect the
        knowledge of this endpoint as admin only endpoints might be hidden.

        """
        r = client.get(
            url_for('api.user_list', page=1, _external=False),
            headers=get_auth_headers(user),
        )

        assert r.status_code == 404

    def test_post_user(self, client, json_headers):
        """
        verify user creation.
        Verify new users don't have email confirmed.
        Verify new users have basic user permissions.
        """
        user_data = fake.ob_user()

        r = client.post(
            url_for('api.user_post'),
            headers=json_headers,
            json=user_data
        )

        assert r.status_code == 201

        u: User = User.query.filter_by(email=user_data['email']).first()

        assert u.id is not None
        assert not u.confirmed
        assert u._permissions == json.dumps(BasicUserRoles.USER)

    # def test_post_user_confirmation_email(self, client, json_headers, get_auth_headers):
    #     with mail.record_messages() as outbox:
    #         user_data = fake.ob_user()
    #
    #         r = client.post(
    #             url_for('api.user_post'),
    #             headers=json_headers,
    #             json=user_data
    #         )
    #
    #         u: User = User.query.filter_by(email=user_data['email']).first()
    #
    #         assert u.id is not None
    #         assert not u.confirmed
    #         assert u._permissions == json.dumps(BasicUserRoles.USER)
    #
    #         soup = BeautifulSoup(outbox[-1].html, 'html.parser')
    #         for a in soup.find_all('a'):
    #             if a.text == 'Click Here':
    #                 link = a.attrs['href']
    #
    #         r = client.get(
    #             link,
    #             headers=get_auth_headers(user_data),
    #         )
    #
    #         assert r.status_code == 200

    def test_post_user_no_email(self, client, json_headers):
        """
        Verify that a user creation requires an email
        """
        user_data = fake.ob_user()
        del user_data['email']
        r = client.post(
            url_for('api.user_post'),
            headers=json_headers,
            json=user_data
        )

        assert r.status_code == 400
        assert 'email' in r.json['message'].lower()

    def test_post_user_no_username(self, client, json_headers):
        """
        Verify that a user creation requires a username
        """
        user_data = fake.ob_user()
        del user_data['username']
        r = client.post(
            url_for('api.user_post'),
            headers=json_headers,
            json=user_data
        )

        assert r.status_code == 400
        assert 'username' in r.json['message'].lower()

    def test_post_user_no_password(self, client, json_headers):
        """
        Verify that a user creation requires a password
        """
        user_data = fake.ob_user()
        del user_data['password']
        r = client.post(
            url_for('api.user_post'),
            headers=json_headers,
            json=user_data
        )

        assert r.status_code == 400
        assert 'password' in r.json['message'].lower()

    def test_post_user_no_password_no_username(self, client, json_headers):
        """
        Confirm that error message contains all parameters that were
        left out.
        """
        user_data = fake.ob_user()
        del user_data['password']
        del user_data['username']
        r = client.post(
            url_for('api.user_post'),
            headers=json_headers,
            json=user_data
        )

        assert r.status_code == 400
        assert 'password' in r.json['message'].lower()
        assert 'username' in r.json['message'].lower()
# @TODO this is not complete... need a lot more user testing.
