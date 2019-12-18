from django.contrib import admin

# Register your models here.

from .models import BarPost, Fotos, PostRelations


def status_winner(modeladmin, request, queryset):
	queryset.update(status='W')

def status_refused(modeladmin, request, queryset):
	queryset.update(status='R')


class PostRelationsAdmin(admin.ModelAdmin):
	list_filter = ('status',)
	list_display = ('event','instaaccount','status','createTime',)
	actions = [status_winner, status_refused]



admin.site.register(BarPost)
admin.site.register(Fotos)
admin.site.register(PostRelations, PostRelationsAdmin)
