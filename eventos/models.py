from django.conf import settings
#m django.core.validators import RegexValidator
from django.db import models

User = settings.AUTH_USER_MODEL

#EVENTPOST
TYPE_EVENTPOST = [
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
#EVENT RELATION
STATUS_EVENT = [
    ('2BA', 'To_be_accepted'),
    ('W', 'Winner'),
    ('F', 'Finished'),
    ('R', 'Refused')
]
class InstaStoryPublication(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Events_Users_Storys/', blank=True, null=True)

    def __str__(self):
        return "Instagram story from @" + str(self.person.instaaccount)


class EventPost(models.Model):
    eventOwner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)#owner_ev
    eventType = models.CharField(choices=TYPE_EVENTPOST, default="A", max_length=3)#type_ev
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='Event_Image/', blank=True, null=True)
    company = models.CharField(max_length=30)
    slug = models.SlugField(default=id(True), max_length=255, unique=True)
    desc = models.CharField(null=True, blank=True, max_length=255, verbose_name="Descripcion")
    users = models.ManyToManyField(User, blank=True, verbose_name="list of users", related_name="+")
    createTime = models.DateTimeField(auto_now=True)
    posts = models.ManyToManyField(InstaStoryPublication, blank=True, verbose_name="publicaciones")
    usersWinners = models.ManyToManyField(User, blank=True, verbose_name="list of users Winners", related_name="+")#usersWinners
    status = models.CharField(choices=STATUS_EVENTPOST, default="2BO", max_length=3)
    stock = models.IntegerField(default=0)
    scoring = models.IntegerField(default=0)
    stockW = models.IntegerField(default=0)
    text = models.CharField(null=True, blank=True, max_length=255, verbose_name="Text to retrieve user information")

    def __str__(self):
        return self.title

class PostRelations(models.Model):
    person = models.ForeignKey(User, default=1, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey(EventPost, default=1, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_EVENT, default="2BA", max_length=3)
    notificationToken = models.CharField(max_length=255, blank=True, null=True)
    story = models.ForeignKey(InstaStoryPublication, blank=True, null=True, on_delete=models.SET_NULL)
    userInfo = models.CharField(max_length=26, verbose_name="Data to save", blank=True)
    

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
