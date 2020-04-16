from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model

from .models import Company, EmailConfirmed, Profile

USER = get_user_model()

class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = USER

admin.site.register(USER, UserAdmin)
admin.site.register(Profile)
admin.site.register(EmailConfirmed)
admin.site.register(Company)
