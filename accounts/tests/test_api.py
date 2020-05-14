from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import EmailConfirmed, Profile, User


class ApiAccountRegistrationTests(APITestCase):

    def test_for_registration_for_common_user(self):
        end_point = "/api/accounts/register"
        registration_data = {
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "case",
            "instaAccount": "@test",
            "password": "testpassword",
            "password2": "testpassword",
            "role": 1
        }
        response = self.client.post(end_point, registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="test@test.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "case")
        self.assertEqual(user.role, 1)

        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.instaAccount, "@test")


class ApiAccountAuthenticationTests(APITestCase):
    """ This class is entended to test all end points regarding accounts that require authentication """

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def setUp(self):
        self.credentials = {
            "email": "testdiferentthanothers@test.com",
            "password": "secret"
        }
        self.user = User.objects.create_user(
            email=self.credentials['email'],
            password=self.credentials['password'],
            first_name="oliver",
            last_name="twist",
        )
        self.email_confirmed, _ = EmailConfirmed.objects.get_or_create(user=self.user)
        self.email_confirmed.confirmed = True
        self.email_confirmed.save()
        self.token = Token.objects.get(user=self.user)
        self.api_authentication()


    def test_log_in_and_response_token(self):
        end_point = "/api/accounts/login"
        log_in_data = {
            'username': self.credentials['email'],
            'password': self.credentials['password']
        }

        response = self.client.post(end_point, log_in_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)
