import secrets
import os
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save

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

def path_and_rename(instance, filename):
    upload_to = 'to_process'
    # get filename
    # if instance.pk:
    filenameAux = '{}.{}.{}'.format(str(instance.pk), str(instance.person.id), instance.person.profile.instaAccount)
    # else:
    # set filename as random string
    #   filename = '{}.{}'.format(uuid4().hex)
    # return the whole path to the file
    return os.path.join(upload_to, filenameAux)

class InstaStoryPublication(models.Model):
    person = models.ForeignKey(USER, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=path_and_rename,
        blank=True,
        null=True
    )
    processedImage = models.ImageField(
        upload_to='processed/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # TODO: CHECK !!!!!!
        return "Instagram story from @" + str(self.person.profile.instaAccount)


class Event(models.Model):
    eventOwner = models.ForeignKey(USER, on_delete=models.CASCADE, default=1)
    eventType = models.CharField(choices=TYPE_EVENT, default="A", max_length=3)
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
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
    startDate = models.DateTimeField(verbose_name="Inicia", blank=True, null=True)
    endDate = models.DateTimeField(verbose_name="Finaliza", blank=True, null=True)

    def __str__(self):
        return str(self.slug)

    def save(self, **kwargs):
        self.slug = "%s-%s" % (self.title.lower(), self.pk)
        super(Event, self).save(**kwargs)


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
    exchange_code = models.CharField(
        verbose_name="Code to recieve benefit",
        max_length=8,
        blank=True,
        null=True
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

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            id_string = str(instance.id)
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            instance.exchange_code = (random_str + id_string)[-8:]
            instance.save()


post_save.connect(Post.post_create, sender=Post)
