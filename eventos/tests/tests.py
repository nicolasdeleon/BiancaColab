from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from accounts.models import User, EmailConfirmed, Profile
from eventos.models import Event, Post


class ApiEvenCreateTests(APITestCase):
    def setUp(self):
        self.credentials = {
            "email": "userforevent@test.com",
            "password": "secret"
        }
        self.user = User.objects.create_user(
            email=self.credentials['email'],
            password=self.credentials['password'],
            first_name="oliver",
            last_name="twist",
            role="1"
        )

        # THIS SHOULD BE CHANGED IF WE ARE USING CONFIRMATION EMAIL FOR USERS
        self.email_confirmed, _ = EmailConfirmed.objects.get_or_create(user=self.user)
        self.email_confirmed.confirmed = True
        self.email_confirmed.save()
        self.token = Token.objects.get(user=self.user)
        self.profile = Profile(user=self.user, instaAccount="insta").save()
        self.event = Event(eventOwner=self.user, eventType="A", title="title to watch", status="O")
        self.event.save()

    def api_Authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_a_for_create_event(self):
        self.api_Authentication()
        end_point = "/api/eventos/create_event/"
        body = {
            "status": "O",
            "stock": 99,
            "title": "tituloapitest",
            "type": "A"
        }
        response = self.client.post(end_point, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_b_for_get_events(self):
        self.api_Authentication()

        end_point = "/api/eventos/all_events/"

        response = self.client.get(end_point)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_c_for_watch_event(self):
        self.api_Authentication()

        end_point = "/api/eventos/all_events/"
        response = self.client.get(end_point)

        end_point = "/api/accounts/eventWatch"
        body = {
             'event_pk': 3,
             'notToken': '1'
         }
        response = self.client.post(end_point, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_d_for_add_user_to_event(self):
        self.api_Authentication()
        pk = Event.objects.get(eventOwner=self.user).pk
        end_point = "/api/eventos/adduser"
        body = {
            "pk": pk,
            "notificationToken": "1"
        }
        response = self.client.post(end_point, body)
        pk = Event.objects.get(eventOwner=self.user).pk
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_e_for_fin_event(self):
        self.api_Authentication()
        self.test_d_for_add_user_to_event()
        end_point = "/api/eventos/all_events/"
        response = self.client.get(end_point)
        post = Post.objects.get(person=self.user)
        post.status = "W"
        post.save()
        pk = Event.objects.get(eventOwner=self.user).pk
        end_point = "/api/eventos/finalize_event/"
        body = {
            'pk': pk,
            'data4Company': '11110144123'
         }
        response = self.client.post(end_point, body)
        post = Post.objects.get(person=self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.status, "F")
