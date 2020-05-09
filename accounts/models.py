""" Accounts Models """
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token


class usermanager(BaseUserManager):
    """ Standard User Manager """
    def create_user(
        self,
        email,
        first_name,
        last_name,
        role=1,
        password=None,
        is_active=True,
        is_staff=False,
        is_admin=False
    ):
        """ Standard User Fields """

        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not password:
            raise ValueError("Users must have a password")

        person = self.model(
            email=self.normalize_email(email),
        )
        person.first_name = first_name
        person.last_name = last_name
        person.full_name = first_name + ' ' + last_name
        person.set_password(password)
        person.staff = is_staff
        person.admin = is_admin
        person.active = is_active
        person.role = role
        person.save(using=self._db)

        return person

    def create_staffuser(self, email, first_name, last_name, password=None):
        """ Staff User Fields """

        person = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True
        )

        return person

    def create_superuser(self, email, first_name, last_name, password=None):
        """ Super User / Owner Fields """

        person = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_admin=True,
            role=0,
        )
        return person


ROLES = [
    (0, 'Admin'),
    (1, 'User'),
    (2, 'Company'),
    (3, 'Validator')
]


class User(AbstractBaseUser):
    """ Custom user extends abstractBaseUser from django auth.models"""
    role = models.IntegerField(choices=ROLES, default=1)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=125)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reset_password_token = models.CharField(
        max_length=22,
        blank=True,
        default=0
    )

    # Remplaza el username field de django default como tmb password.

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    objects = usermanager()

    def __str__(self):
        """ User object name """
        return self.email

    def get_full_name(self):
        """ References user full name """
        return self.full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Company(models.Model):
    """ Extend extra fields for company of user rather than change user model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=40, default="", blank=True, null=True)
    instaAccount = models.CharField(max_length=255, unique=True, null=True)
    companyName = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    """ Extend extra fields of user rather than change user model """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(verbose_name='Amount of followers', blank=True, null=True)
    likes = models.FloatField(verbose_name='Promediated likes per publication', blank=True, null=True)
    zone = models.CharField(verbose_name='Location', max_length=255, blank=True)
    scoring = models.IntegerField(verbose_name='Overall event score', blank=True, default=0)
    phone = models.CharField(max_length=40, default="", blank=True, null=True)
    instaAccount = models.CharField(max_length=255, unique=True, null=True)
    birthDate = models.DateTimeField(verbose_name="Fecha de nacimiento", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    eventWatchList = ArrayField(
            models.CharField(max_length=30, blank=True, default="0"),
            size=50,
            blank=True,
            default=list
        )
    notificationToken = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ' - confirmed: ' + str(self.confirmed)

    def activate_user_email(self):
        activation_url = "https://biancaapp-ndlc.herokuapp.com/accounts/activate/%s" % (self.activation_key)
        context = {
            "activation_url": activation_url,
        }
        subject = "Confirmá tu Cuenta"
        message = render_to_string("activation_message.html", context)
        self.email_user(subject, text_body='', html_body=message, from_email=settings.SUPPORT_EMAIL)

    def email_user(self, subject, text_body, html_body, from_email=None):
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=[self.User.email],
            body=text_body
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
