from django.db import models
from django.utils.text import slugify

from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from django.core.validators import RegexValidator

user = settings.AUTH_USER_MODEL

STATUS_EVENT ={
    ('2BA','To_be_accepted'),
    ('W','Winner'),
    ('F','Finished'),
    ('R','Refused')
}

STATUS_EVENTPOST ={
    ('2BO','To_be_open'),
    ('O','Open'),
    ('C','Close'),
    ('F','Finished')
}

class fotos(models.Model):
    updloader = models.ForeignKey(user, default = 1, blank = True, on_delete=models.CASCADE)
    image = models.FileField(upload_to='image/',blank=True,null=True)

class eventpost(models.Model):
    title = models.CharField(max_length = 30)
    company = models.CharField(max_length = 30)
    slug = models.SlugField(default = id(True),max_length=255, unique=True)
    desc = models.CharField(null=True, blank= True, max_length = 255)
    users = models.ManyToManyField(user,blank=True,verbose_name="list of users",related_name="+")
    createTime = models.DateTimeField(auto_now = True)
    posts = models.ManyToManyField(fotos, blank = True, verbose_name="publicaciones")
    code = models.CharField(validators=[RegexValidator(regex='^.{5}$', message='Length has to be 5', code='nomatch')],max_length = 5,null=True,unique=True)
    users_winners = models.ManyToManyField(user,blank=True,verbose_name="list of users Winners",related_name="+")
    status =  models.CharField(choices = STATUS_EVENTPOST, default = "2BO", max_length=3)
    stock = models.IntegerField(default = 0)
    scoring = models.IntegerField(default = 0)
    stockW = models.IntegerField(default = 0)

    def __str__(self):
        return self.title

class postrelations(models.Model):
    person = models.ForeignKey(user, default = 1, blank = True, on_delete=models.CASCADE)
    event = models.ForeignKey(eventpost, default = 1, blank = True, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now = True)
    winer_code = models.CharField(max_length=20,verbose_name="Code to Retrieve")
    status = models.CharField(choices = STATUS_EVENT, default = "2BA", max_length=3)
    notificationToken = models.CharField(max_length=40,blank = True, null=True)

    class Meta:
        ordering = ['-createTime']

    def get_event_url(self):
        return self.slug

    def get_edit_url(self):
        return f"edit/{self.slug}" 

    def get_delete_url(self):
        return f"delete/{self.slug}"       

    def __str__(self):
        return (self.event.title + ' - ' + self.person.instaaccount)

    def instaaccount(self):
        return self.person.instaaccount
