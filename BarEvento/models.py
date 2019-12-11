from django.db import models
from django.utils.text import slugify

from django.conf import settings
from django.contrib.postgres.fields import ArrayField


User = settings.AUTH_USER_MODEL
"""
STATUS_EVENT ={
    ('To_be_accepted','0'),
    ('Winner_new','1'),
    ('Winner_end','2'),
    ('Refused','3')

}
"""
STATUS_EVENT ={
    ('2BA','To_be_accepted'),
    ('W','Winner'),
    ('F','Finished'),
    ('R','Refused')
}



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
    is_finalized = models.BooleanField(default=False)
    users_winners = models.ManyToManyField(User,blank=True,verbose_name="list of users Winners",related_name="+")
      
    #Overrides Call of object by its title
    def __str__(self):
        return self.title

class PostRelations(models.Model):
    person = models.ForeignKey(User, default = 1, blank = True, on_delete=models.CASCADE)
    event = models.ForeignKey(BarPost, default = 1, blank = True, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now = True)
    code = models.CharField(max_length = 5,null=True) #No se muy bien porque este.
    winer_code = models.CharField(max_length=20,verbose_name="Code to Retrieve")
    invite_reason = models.CharField(max_length=6,blank=True)
    status = models.CharField(choices = STATUS_EVENT, default = "2BA", max_length=3)
    is_finalized = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-createTime']

    def get_event_url(self):
        return self.slug

    def get_edit_url(self):
        return f"edit/{self.slug}" 

    def get_delete_url(self):
        return f"delete/{self.slug}"       
    
    #Overrides Call of object by its EVENT_TITLE - INSTAACCOUNT
    def __str__(self):
        return (self.event.title + ' - ' + self.person.instaaccount)



    #override save method to define a unique slug
   # def save(self, *args, **kwargs):
   #     super(BarPost, self).save(*args, **kwargs)
   #     if not self.slug:
   #         self.slug = slugify(self.company + "-" + str(self.id))
   #         self.save()