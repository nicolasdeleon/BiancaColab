from django.db import models
from django.utils.text import slugify

from django.conf import settings
from django.contrib.postgres.fields import ArrayField


User = settings.AUTH_USER_MODEL

class Fotos(models.Model):
    updloader = models.ForeignKey(User, default = 1, blank = True, on_delete=models.CASCADE)
    image = models.FileField(upload_to='image/',blank=True,null=True)

class BarPost(models.Model):
    title = models.CharField(max_length = 30)
    company = models.CharField(max_length = 30)
    slug = models.SlugField(default = id(True),max_length=255, unique=True)
    desc = models.CharField(null=True, blank= True, max_length = 255)
    users = models.ManyToManyField(User,blank=True,verbose_name="list of users",related_name="+")
    createTime = models.DateTimeField(auto_now = True)
    posts = models.ManyToManyField(Fotos, blank = True, verbose_name="publicaciones")
    dia = models.TextField()
    code = models.CharField(max_length = 5,null=True)
    is_finalized = models.BooleanField(default=False,blank=True)
    users_winners = models.ManyToManyField(User,blank=True,verbose_name="list of users Winners",related_name="+")
    
    
    class Meta:
        ordering = ['-createTime']

    def get_event_url(self):
        return self.slug

    def get_edit_url(self):
        return f"edit/{self.slug}" 

    def get_delete_url(self):
        return f"delete/{self.slug}"       

    #override save method to define a unique slug
   # def save(self, *args, **kwargs):
   #     super(BarPost, self).save(*args, **kwargs)
   #     if not self.slug:
   #         self.slug = slugify(self.company + "-" + str(self.id))
   #         self.save()
