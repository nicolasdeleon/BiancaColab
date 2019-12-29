from django.contrib import admin

# Register your models here.

from .models import eventpost, fotos, postrelations

from django.contrib import messages
'''DEBUG	debug
INFO	info
SUCCESS	success
WARNING	warning
ERROR	error'''

def status_winner(modeladmin, request, queryset):
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

		   
		     #evento = eventpost.objects.get(person = pr.event )
		     



	#evento.stockW +=1

	#queryset.update(status='W')

def status_refused(modeladmin, request, queryset):
	queryset.update(status='R')


class postrelationsadmin(admin.ModelAdmin):
	list_filter = ('status',)
	list_display = ('event','instaaccount','status','createTime',)
	actions = [status_winner, status_refused]



admin.site.register(eventpost)
admin.site.register(fotos)
admin.site.register(postrelations, postrelationsadmin)
