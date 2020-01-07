from django.contrib import admin

# Register your models here.

from .models import eventpost, fotos, postrelations

from django.contrib import messages
'''DEBUG	debug
INFO	info
SUCCESS	success
WARNING	warning
ERROR	error'''

def set_status_winner(modeladmin, request, queryset):
		for q in queryset:
				if q.status == "2BA":
						event = q.event
						if event.stock << event.stockW and event.status == "O":
						 event.stockW +=1
						 event.save()
						 q.status='W'
						 q.save()
						 messages.success(request, 'Se marcó como winner')
						 if event.stock == event.stockW:
						 	event.status = "C"
						 	event.save()
						else:
						 #event.status == "C"
						 messages.error(request, 'Evento concluido')
				else:
					messages.error(request, 'Relación ya marcada como ganadora')


def set_status_refused(modeladmin, request, queryset):
	queryset.update(status='R')

def set_status_finished(modeladmin, request, queryset):
		for q in queryset:
				if q.status == "W":
						event = q.event
						q.status='F'
						q.save()
						messages.success(request, 'Se marcó como pagada')
				else:
					messages.error(request, 'Relación no ganadora')
					


class postrelationsadmin(admin.ModelAdmin):
	list_filter = ('status',)
	list_display = ('event','instaaccount','status','createTime',)
	actions = [set_status_winner, set_status_refused, set_status_finished]



admin.site.register(eventpost)
admin.site.register(fotos)
admin.site.register(postrelations, postrelationsadmin)
