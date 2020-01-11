from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class usermanager(BaseUserManager):
	def create_user(self, 
		email, 
		first_name, 
		last_name,
		instaaccount,
		birthDate = "2020-1-1",  
		password = None, 
		is_active = True,
		is_staff = False, 
		is_admin = False):
		
		if not email:
			raise ValueError("Users must have an email address")
		if not instaaccount:
			raise ValueError("Users must have a Instagram ccount")
		if not first_name:
			raise ValueError("Users must have a first name")
		if not last_name:
			raise ValueError("Users must have a last name")
		if not password:
			raise ValueError("Users must have a password")

		person = self.model(
			email = self.normalize_email(email),
			)
		person.instaaccount = instaaccount
		person.first_name = first_name
		person.last_name = last_name
		person.full_name = first_name + ' ' + last_name
		person.set_password(password)
		person.birthDate = birthDate
		person.staff = is_staff
		person.admin = is_admin
		person.active = is_active
		person.save(using=self._db)
		
		return person

	def create_staffuser(self, 
		email, 
		instaaccount, 
		first_name,
		last_name,
		password=None):
		
		person = self.create_user(
			email,
			instaaccount = instaaccount,
			first_name = first_name,
			last_name = last_name,
			password = password,
			is_staff = True)
		
		return person

	def create_superuser(self,
		email, 
		instaaccount,
		first_name,
		last_name,
		password=None):
		
		person = self.create_user(
			email,
			instaaccount = instaaccount,
			first_name = first_name,
			last_name = last_name,
			password = password,
			is_staff = True,
			is_admin = True)
		
		return person


class user(AbstractBaseUser):

	email = models.EmailField(max_length= 255, unique = True)
	full_name = models.CharField(max_length = 255, default="missing")
	first_name = models.CharField(max_length=120, default="missing")
	last_name = models.CharField(max_length=125, default="missing")
	birthDate = models.DateTimeField(default=timezone.now)
	active = models.BooleanField(default = True)
	staff  = models.BooleanField(default = False)
	admin = models.BooleanField(default = False)
	instaaccount = models.CharField(max_length= 255,unique=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	scoring = models.IntegerField(default = 0)
	reset_password_token = models.CharField(max_length= 22, default = 0)

	# remplaza el username field de django default como tmb password

	USERNAME_FIELD = 'email'

	# Requested by superuser and ordinary users. Fields such as email and password are Required as well
	REQUIRED_FIELDS = [
		'first_name',
		'last_name',
		'instaaccount'
		] 

	objects = usermanager()

	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.full_name

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