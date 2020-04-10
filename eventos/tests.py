from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from accounts.models import User, EmailConfirmed

#from eventos.models import eventpost
# Create your tests here.

class ApiEvenCreateTests(APITestCase):

    def setUp(self):
        self.credentials = {
            "email" : "userforevent@test.com",
            "password" : "secret"
        }
        self.user = User.objects.create_user(
            email=self.credentials['email'],
            password=self.credentials['password'],
            first_name="oliver",
            last_name="twist",
            role="1"
        )
        # THIS SHOULD BE CHANGED IF WE ARE USING CONFIRMATION EMAIL FOR USERS
        self.email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=self.user)
        self.email_confirmed.confirmed = True
        self.email_confirmed.save()
        self.token = Token.objects.get(user=self.user)
        self.api_Authentication()
        #self.test_log_in()
        self.test_for_create_event()
        self.test_for_add_user_to_event()

    def api_Authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
    
    # def test_log_in(self):
    #     end_point = "/api/accounts/login"
    #     log_in_data = {
    #         'username' : self.credentials['email'],
    #         'password' : self.credentials['password']
    #     }

    #     response = self.client.post(end_point, log_in_data)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['token'], self.token.key)    

    def test_for_create_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        end_point ="/api/eventos/create_event/"
        body = {
            "status" : "O",
            "stock" :99,
            "title": "tituloapitest",
            "type": "A"
        }
        response = self.client.post(end_point, body)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#class ApiEventAddUserTests(APITestCase):

	 # Tests
    def test_for_add_user_to_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        end_point = "/api/eventos/adduser"
        body = {
            "pk" : 1,   
            "notificationToken" : "1"
        }
        response = self.client.post(end_point, body)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)