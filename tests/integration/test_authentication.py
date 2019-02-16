"""
Created: 2/7/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import base64


class TestAuthentication:

    def test_not_logged_in(self, client):
        """
        Verify that credentials are needed to access the API
        """
        r = client.get('/api/v1/')
        assert r.status_code == 401

    def test_login(self, client, user, get_auth_headers):
        """
        A Valid login
        """
        valid_credentials = base64.b64encode(
            f'{user["email"]}:{user["password"]}'.encode()
        ).decode('utf-8')

        r = client.get(
            '/api/v1/',
            headers=get_auth_headers(user)
        )
        assert r.status_code == 200

    def test_invalid_password(self, client, user):
        """
        An invalid password
        """
        invalid_password = base64.b64encode(
            f'{user["email"]}:invalid'.encode()
        ).decode('utf-8')

        r = client.get('/api/v1/', headers={
            'Authorization': f'Basic {invalid_password}'
        })
        assert r.status_code == 401

    def test_invalid_email(self, client, user):
        """
        An invalid email
        """
        invalid_email = base64.b64encode(
            f'invalid:{user["password"]}'.encode()
        ).decode('utf-8')

        r = client.get('/api/v1/', headers={
            'Authorization': f'Basic {invalid_email}'
        })
        assert r.status_code == 401
