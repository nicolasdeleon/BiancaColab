from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import User, EmailConfirmed


# Create your tests here.

class ApiAccountRegistrationTests(APITestCase):

    # Note: ¡¡MAKE SURE THE FRONT END SENDING THE DATA KNOWS THERE HAS BEEN A CHANGE BEFORE MAKING CHANGES!!

    # Tests that api registration end point is storing the right information about a user
    def test_for_registration(self):
        end_point = "/api/accounts/register"
        registration_data = {
            "email" : "test@test.com",
            "first_name" : "test",
            "last_name" : "case",
            "instaAccount" : "@test",
            "birth_date" : timezone.datetime(1997, 1, 23, 00, 00, 00, 00),
            "password" : "testpassword",
            "password2" : "testpassword"
        }
        response = self.client.post(end_point, registration_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ApiAccountAuthenticationTests(APITestCase):
    """ This class is entended to test all end points regarding accounts that require authentication """

    def setUp(self):
        self.credentials = {
            "email" : "testdiferentthanothers@test.com",
            "password" : "secret"
        }
        self.user = user.objects.create_user(
            email=self.credentials['email'],
            password=self.credentials['password'],
            instaaccount="@test22222",
            first_name="oliver",
            last_name="twist",
        )
        # THIS SHOULD BE CHANGED IF WE ARE USING CONFIRMATION EMAIL FOR USERS
        self.email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=self.user)
        self.email_confirmed.confirmed = True
        self.email_confirmed.save()
        self.token = Token.objects.get(user=self.user)
        self.api_Authentication()

    def api_Authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    # Actual authentication assertions

    # Api Log In Test:
    def test_log_in(self):
        end_point = "/api/accounts/login"
        log_in_data = {
            'username' : self.credentials['email'],
            'password' : self.credentials['password']
        }

        response = self.client.post(end_point, log_in_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)
