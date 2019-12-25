from django.contrib import admin

# Register your models here.

from .models import eventpost, fotos, postrelations


def status_winner(modeladmin, request, queryset):
	queryset.update(status='W')

def status_refused(modeladmin, request, queryset):
	queryset.update(status='R')


class postrelationsadmin(admin.ModelAdmin):
	list_filter = ('status',)
	list_display = ('event','instaaccount','status','createTime',)
	actions = [status_winner, status_refused]



admin.site.register(eventpost)
admin.site.register(fotos)
admin.site.register(postrelations, postrelationsadmin)
