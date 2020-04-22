from django.contrib import admin, messages
from exponent_server_sdk import (DeviceNotRegisteredError, PushClient,
                                 PushMessage, PushResponseError,
                                 PushServerError)
from requests.exceptions import ConnectionError, HTTPError

from .models import Event, InstaStoryPublication, Post


def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message))
    except PushServerError as exc:
        raise

def set_status_winner(modeladmin, request, queryset):
    for q in queryset:
        if q.status == "2BA":
            event = q.event
            if event.stock > event.activeParticipants and event.status == "O":
                event.save()
                q.status = 'W'
                var_token = q.notificationToken
                q.save()
                var_token = q.notificationToken
                messages.success(request, 'Se marcó como winner')
                try:
                    send_push_message(token=var_token, message='Aprobado! Ahora busca tu beneficio!')
                except:
                    return
            else:
                messages.error(request, 'Evento concluido')
        else:
            messages.error(request, 'Relación ya finalizada')


def set_status_refused(modeladmin, request, queryset):
    queryset.update(status='R')

def set_status_finished(modeladmin, request, queryset):
    for q in queryset:
        if q.status == "W":
            q.status = 'F'
            q.save()
            # var_token = q. notificationToken
            # send_push_message(token=var_token, message='Ganaste' )
            messages.success(request, 'Se marcó como finalizada')
        else:
            messages.error(request, 'Relación no ganadora')


class PostAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('instaAccount', 'event', 'status', 'createTime')
    actions = [set_status_winner, set_status_refused, set_status_finished]


class InstaStoryPublicationAdmin(admin.ModelAdmin):
    list_filter = ('person',)
    list_display = ('person', )

admin.site.register(Event)
admin.site.register(Post, PostAdmin)
admin.site.register(InstaStoryPublication, InstaStoryPublicationAdmin)
