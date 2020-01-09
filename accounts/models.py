from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,

)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class usermanager(BaseUserManager):
	def create_user(self, email, instaaccount=None,full_name=None, password = None, is_active =True,is_staff=False, is_admin=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not instaaccount:
			raise ValueError("Users must have an instaaccount")
		if not full_name:
			raise ValueError("Users must have a full name")
		if not password:
			raise ValueError("Users must have a password")

		user_obj = self.model(
			email = self.normalize_email(email),
			)
		user_obj.instaaccount = instaaccount,
		user_obj.full_name = full_name
		user_obj.set_password(password)
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.active = is_active
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, instaaccount, full_name, password=None):
		user = self.create_user(
			email,
			instaaccount=instaaccount,
			full_name =full_name,
			password=password,
			is_staff=True)
		return user

	def create_superuser(self,email, instaaccount,full_name,password=None):
		user = self.create_user(
			email,
			instaaccount=instaaccount,
			full_name =full_name,
			password=password,
			is_staff=True,
			is_admin=True)
		return user


class user(AbstractBaseUser):
	#id
	#pass
	#lastlogin
	email = models.EmailField(max_length= 255, unique = True)
	full_name = models.CharField(max_length = 255)
<<<<<<< Updated upstream
=======
	first_name = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255,blank=True)
	birthDate = models.DateTimeField(auto_now=False,default=timezone.now)
>>>>>>> Stashed changes
	birthDate = models.DateTimeField(auto_now=False,default=timezone.now)
	active = models.BooleanField(default = True) #can login
	staff  = models.BooleanField(default = False) #staff user not suepruser
	admin = models.BooleanField(default = False) #superuser
	instaaccount = models.CharField(max_length= 255,unique=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	scoring = models.IntegerField(default = 0)
	reset_password_token = models.CharField(max_length= 10, default = 0)
#	scoring = models.IntegerField(default = 1)
	#confirm  = models.BolleanField(defalut=False)
	#

	USERNAME_FIELD = 'email'
	#remplaza el username field de django default como tmb password

	REQUIRED_FIELDS = ['full_name','instaaccount'] #cualquier otro field q si o si sea necesario

	objects = usermanager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.ful_name

	def get_instaaccount(self):
		return self.instaaccount


	def has_perm(self,perm,obj=None):
		return True

	def has_module_perms(self,app_label):
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
	
class profile(models.Model):
	user = models.OneToOneField(user,on_delete=models.CASCADE)
	#extends extra field of user with other info
	#tiene que tener la menor cantidad de cambios posibles user model}

@receiver(post_save,sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance) 