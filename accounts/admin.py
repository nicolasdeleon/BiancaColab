from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from .models import EmailConfirmed

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
	search_fields = ['email']
	class Meta:
		model = User

admin.site.register(User,UserAdmin)
admin.site.register(EmailConfirmed)

