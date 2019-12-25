from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class useradmin(admin.ModelAdmin):
	search_fields = ['email']
	class Meta:
		model = User



admin.site.register(user,UserAdmin)

