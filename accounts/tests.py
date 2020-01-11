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


# Create your tests here.
class ApiAccountRegistrationTests(APITestCase):

    # Note: ¡¡MAKE SURE THE FRONT END SENDING THE DATA KNOWS THERE HAS BEEN A CHANGE BEFORE MAKING CHANGES!!

    # Tests that api registration end point is storing the right information about a user
    def test_for_registration(self):
        registration_data = {
            "email" : "test@test.com",
            "first_name" : "test",
            "last_name" : "case",
            "instaaccount" : "@test",
            "birthDate" : timezone.datetime(1997,1,23,00,00,00,00),
            "password" : "testpassword",
            "password2" : "testpassword"
        }
        response = self.client.post("/api/accounts/register",registration_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

"""
class ApiAccountAuthenticationTests(APITestCase):

    # This class is entended to test all end points regarding accounts that require authentication

    def setUp(self):
        self.user = user.objects.create_user(
            "test@test.com",
            "@test",
            "test"
        )
"""