from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from accounts.models import Profile

USER = settings.AUTH_USER_MODEL

TYPE_EVENT = [
    ('A', 'Short'),
    ('B', 'Long'),
    ('T', 'Test')
]

STATUS_EVENT = [
    ('2BO', 'To_be_open'),
    ('O', 'Open'),
    ('C', 'Close'),
    ('F', 'Finished')
]

STATUS_POST = [
    ('2BA', 'To_be_accepted'),
    ('W', 'Winner'),
    ('F', 'Finished'),
    ('R', 'Refused')
]


class InstaStoryPublication(models.Model):
    person = models.ForeignKey(USER, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='Events_Users_Storys/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # TODO: CHECK !!!!!!
        return "Instagram story from @" + str(self.person.profile_instaAccount)


class Event(models.Model):
    eventOwner = models.ForeignKey(USER, on_delete=models.CASCADE, default=1)
    eventType = models.CharField(choices=TYPE_EVENT, default="A", max_length=3)
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='Event_Image/', blank=True, null=True)
    slug = models.SlugField(default=id(True), max_length=255, unique=True)
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Descripción"
    )
    createTime = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posts = models.ManyToManyField(
        InstaStoryPublication,
        blank=True,
        verbose_name="publicaciones"
    )
    usersWinners = models.ManyToManyField(
        USER,
        blank=True,
        verbose_name="list of users Winners",
        related_name="+"
    )
    status = models.CharField(
        choices=STATUS_EVENT,
        default="2BO",
        max_length=3
    )
    stock = models.IntegerField(default=50)
    scoring = models.IntegerField(default=0)
    activeParticipants = models.IntegerField(default=0)
    benefitDescription = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="How to retrieve benefit"
    )
    tags = ArrayField(
            models.CharField(max_length=30, blank=True, default="0"),
            size=50,
            blank=True,
            default=list
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    person = models.ForeignKey(
        USER,
        default=1,
        blank=True,
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        Profile,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(Event, default=1, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_POST, default="2BA", max_length=3)
    notificationToken = models.CharField(max_length=255, blank=True, null=True)
    instagramStory = models.ForeignKey(
        InstaStoryPublication,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    data4Company = models.CharField(
        max_length=26,
        verbose_name="Data company needs to give benefit",
        blank=True
    )
    receivedBenefit = models.BooleanField(
        verbose_name="Has received benefit ?",
        default=False
    )

    class Meta:
        ordering = ['-createTime']

    def get_event_url(self):
        return self.slug

    def get_edit_url(self):
        return f"edit/{self.slug}"

    def get_delete_url(self):
        return f"delete/{self.slug}"

    def __str__(self):
        return self.event.title + ' - ' + self.person.profile.instaAccount

    def instaAccount(self):
        return self.person.profile.instaAccount


    def phone(self):
        return self.person.profile.phone
