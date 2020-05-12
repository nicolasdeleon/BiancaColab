from django.contrib import admin, messages
from exponent_server_sdk import (PushClient, PushMessage,
                                 PushServerError)

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Event, InstaStoryPublication, Post


class PostResource(resources.ModelResource):

    class Meta:
        model = Post
        fields = ('profile__instaAccount', 'event__title', 'status', 'createTime', 'profile__phone')


def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message))
        return response
    except PushServerError as exc:
        raise exc


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
                    send_push_message(
                        token=var_token,
                        message='Felicidades! Ingresa y completá el último paso para recibir tu beneficio'
                    )
                except PushServerError as exc:
                    messages.error(request, str(exc))
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


class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_filter = ('status', 'event__title', )
    list_display = ('instaAccount', 'event', 'status', 'createTime', 'data4Company',)
    actions = [set_status_winner, set_status_refused]
    resource_class = PostResource


class InstaStoryPublicationAdmin(admin.ModelAdmin):
    list_filter = ('person',)
    list_display = ('person', )


admin.site.register(Event)
admin.site.register(Post, PostAdmin)
admin.site.register(InstaStoryPublication, InstaStoryPublicationAdmin)
