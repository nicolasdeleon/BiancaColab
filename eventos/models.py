from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

user = settings.AUTH_USER_MODEL

STATUS_EVENT = [
    ('2BA', 'To_be_accepted'),
    ('W', 'Winner'),
    ('F', 'Finished'),
    ('R', 'Refused')
]
TYPE_EVENT = [
    ('A', 'Short'),
    ('B', 'Long'),
    ('T', 'Test')
]

STATUS_EVENTPOST = [
    ('2BO', 'To_be_open'),
    ('O', 'Open'),
    ('C', 'Close'),
    ('F', 'Finished')
]

class InstaStoryPublication(models.Model):
    person = models.ForeignKey(user, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Events_Users_Storys/', blank=True, null=True)

    def __str__(self):
        return "Instagram story from @" + str(self.person.instaaccount)


class eventpost(models.Model):
    type_ev = models.CharField(choices=TYPE_EVENT, default="A", max_length=3)
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='Event_Image/', blank=True, null=True)
    company = models.CharField(max_length=30)
    slug = models.SlugField(default=id(True), max_length=255, unique=True)
    desc = models.CharField(null=True, blank=True, max_length=255, verbose_name="Descripcion")
    users = models.ManyToManyField(user, blank=True, verbose_name="list of users", related_name="+")
    createTime = models.DateTimeField(auto_now=True)
    posts = models.ManyToManyField(InstaStoryPublication, blank=True, verbose_name="publicaciones")
    users_winners = models.ManyToManyField(user, blank=True, verbose_name="list of users Winners", related_name="+")
    status = models.CharField(choices=STATUS_EVENTPOST, default="2BO", max_length=3)
    stock = models.IntegerField(default=0)
    scoring = models.IntegerField(default=0)
    stockW = models.IntegerField(default=0)
    text = models.CharField(null=True, blank=True, max_length=255, verbose_name="Text to retrieve user information")

    def __str__(self):
        return self.title

class postrelations(models.Model):
    person = models.ForeignKey(user, default=1, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(eventpost, default=1, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now=True)
    winer_code = models.CharField(max_length=20, verbose_name="Code to Retrieve")
    status = models.CharField(choices=STATUS_EVENT, default="2BA", max_length=3)
    notificationToken = models.CharField(max_length=255, blank=True, null=True)
    story = models.ForeignKey(InstaStoryPublication, blank=True, null=True, on_delete=models.SET_NULL)
    user_info = models.CharField(max_length=26, verbose_name="Data to save", blank=True)
    

    class Meta:
        ordering = ['-createTime']

    def get_event_url(self):
        return self.slug

    def get_edit_url(self):
        return f"edit/{self.slug}"

    def get_delete_url(self):
        return f"delete/{self.slug}"

    def __str__(self):
        return self.event.title + ' - ' + self.person.instaaccount

    def instaaccount(self):
        return self.person.instaaccount
