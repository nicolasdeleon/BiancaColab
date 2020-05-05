from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from accounts.models import User, EmailConfirmed, Profile, Company
from eventos.models import Event, Post
from eventos.admin import set_status_winner
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
        self.profile = Profile(user=self.user,instaAccount= "insta").save()
   
        print("test setup")
        print (self.token.key)


    def api_Authentication(self):
        print ("api_Authentication")
        print (self.token.key)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
  
#class ApiCreateEventTest(APITestCase):

    def test_a_for_create_event(self):
        
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        print("test_for_Create_event")
        print(self.token.key)
        end_point ="/api/eventos/create_event/"
        body = {
            "status" : "O",
            "stock" :99,
            "title": "tituloapitest",
            "type": "A"
        }
        response = self.client.post(end_point, body)
        print(response.data)
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#class ApiGetEvents(APITestCase):
    def test_b_for_get_events(self):
        


        
        #self.test_for_create_event(self)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        print("test_for_get_event")
        print(self.token.key)
        self.event = Event(eventOwner=self.user, eventType="A", title="title", status = "O").save(),

        end_point = "/api/eventos/all_events/"

        response = self.client.get(end_point)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_c_for_watch_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        print("test_watch_event")
        self.event = Event(eventOwner=self.user, eventType="A", title="title to watch", status = "O").save(),

        end_point = "/api/eventos/all_events/"
        response = self.client.get(end_point)
        print(response.data)

        end_point = "/api/accounts/eventWatch"
        body = {
             'event_pk' : 3,   
             'notToken' : '1'
         }
        response = self.client.post(end_point, body)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_d_for_add_user_to_event(self):
        #self.test_for_get_events(self)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        print("test_for_add_user_to_event")
        print(self.token.key)
        self.event = Event(eventOwner=self.user, eventType="A", title="title add", status = "O").save(),
        end_point = "/api/eventos/all_events/"

        response = self.client.get(end_point)

        pk = Event.objects.get(eventOwner=self.user).pk
        end_point = "/api/eventos/adduser"
        body = {
            "pk" : pk,   
            "notificationToken" : "1"
        }
        response = self.client.post(end_point, body)
        pk = Event.objects.get(eventOwner=self.user).pk   #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_e_for_fin_event(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        print("test_for fin event")

        self.test_d_for_add_user_to_event()

        end_point = "/api/eventos/all_events/"
        response = self.client.get(end_point)
        print(response.data)

        post = Post.objects.get(person=self.user)
        post.status = "W"
        post.save()
        pk = Event.objects.get(eventOwner=self.user).pk
        
        end_point = "/api/eventos/finalize_event/"
        body = {
             'pk' : pk,   
             'data4Company' : '11110144123'
         }
        response = self.client.post(end_point, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
