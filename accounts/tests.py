import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.api.serializers import RegistrationSerializer
from accounts.models import user
import secrets

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
            "instaaccount" : "@test",
            "birthDate" : timezone.datetime(1997,1,23,00,00,00,00),
            "password" : "testpassword",
            "password2" : "testpassword"
        }
        response = self.client.post(end_point, registration_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ApiAccountAuthenticationTests(APITestCase):

    # This class is entended to test all end points regarding accounts that require authentication
    def setUp(self):
        self.credentials = {
            "email" : "testdiferentthanothers@test.com",
            "password" : "secret"
        }
        self.user = user.objects.create_user(
            email = self.credentials['email'],
            password = self.credentials['password'],
            instaaccount = "@test22222",
            first_name = "oliver",
            last_name = "twist",
        )
        self.token = Token.objects.get(user=self.user)
        self.api_Authentication()

    def api_Authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + self.token.key)
    
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