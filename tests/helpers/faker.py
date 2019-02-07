"""
Created: 2/6/2019
Author: Emiliano Jordan,
        https://github.com/EmilianoJordan
        https://www.linkedin.com/in/emilianojordan/,
        Most other things I'm @emilianojordan
"""
import secrets
import string

from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class Provider(BaseProvider):

    def ob_user(self):
        chars = string.ascii_letters + string.digits
        return {
            'username': self.generator.user_name(),
            'email': self.generator.free_email(),
            'password': ''.join(secrets.choice(chars) for _ in range(15))
        }

fake.add_provider(Provider)