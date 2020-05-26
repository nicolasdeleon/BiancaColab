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
            role=1
        )

        # THIS SHOULD BE CHANGED IF WE ARE USING CONFIRMATION EMAIL FOR USERS
        self.email_confirmed, _ = EmailConfirmed.objects.get_or_create(user=self.user)
        self.email_confirmed.confirmed = True
        self.email_confirmed.save()
        self.token = Token.objects.get(user=self.user)
        self.profile = Profile(user=self.user, instaAccount="insta")
        self.profile.save()
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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


class ValidateCupons(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='email',
            password='password',
            first_name="oliver",
            last_name="twist",
            role="1"
        )
        self.profile = Profile.objects.create(user=self.user, instaAccount="insta")
        self.short_event = Event.objects.create(
            eventOwner=self.user,
            eventType="A",
            title="Evento tipo Local",
            status="O"
        )
        self.short_post = Post.objects.create(
            person=self.user,
            profile=self.profile,
            event=self.short_event,
            status='W'
        )
        self.exchange_code_in_short_event = self.short_post.exchange_code
        self.long_event = Event.objects.create(
            eventOwner=self.user,
            eventType="B",
            title="Event tipo Wabi",
            status="O"
        )
        self.long_post = Post.objects.create(
            person=self.user,
            profile=self.profile,
            event=self.long_event,
            status='W'
        )
        self.exchange_code_in_long_event = self.long_post.exchange_code

    def api_Authentication(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_exchange_code_correct_usage(self):
        self.api_Authentication()
        end_point = "/api/eventos/code-validation"
        body = {
            'code': self.exchange_code_in_short_event
        }
        response = self.client.post(end_point, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], "succesfuly exchanged")

        post = Post.objects.get(pk=self.short_post.pk)
        self.assertEqual(post.status, 'F')
        self.assertEqual(post.receivedBenefit, True)

    def test_not_finishing_long_event_post(self):
        self.api_Authentication()
        end_point = "/api/eventos/code-validation"
        body = {
            'code': self.exchange_code_in_long_event
        }
        response = self.client.post(end_point, body)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        post = Post.objects.get(pk=self.long_post.pk)
        self.assertEqual(post.status, 'W')
        self.assertEqual(post.receivedBenefit, False)

    # TODO: Check company finishing event that isn't his
