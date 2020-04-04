from django.contrib import admin, messages
from exponent_server_sdk import (DeviceNotRegisteredError, PushClient,
                                 PushMessage, PushResponseError,
                                 PushServerError)
from requests.exceptions import ConnectionError, HTTPError

from .models import eventpost, InstaStoryPublication, postrelations


def send_push_message(token, message, extra=None):
    # logger = logging.getLogger(__name__)
    # logger.error("Test!!")
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        # rollbar.report_exc_info(9_1
        #     extra_data={
        #         'token': token,
        #         'message': message,
        #         'extra': extra,
        #         'errors': exc.errors,
        #         'response_data': exc.response_data,
        #     })
        raise
"""
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        # rollbar.report_exc_info(9_!
        #     extra_data={'token': token, 'message': message, 'extra': extra})
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise self.retry(exc=exc)
"""

def set_status_winner(modeladmin, request, queryset):
    for q in queryset:
        if q.status == "2BA":
            event = q.event
            if event.stock << event.stockW and event.status == "O":
                #event.stockW += 1
                #event.save()
                q.status = 'W'
                var_token = q.notificationToken
                q.save()
                var_token = q.notificationToken
                messages.success(request, 'Se marcó como winner')
                if event.stock == event.stockW:
                    event.status = "F"
                    event.save()
                
                try:
                    send_push_message(token=var_token, message='Aprobado! Ahora busca tu beneficio!')
                except:
                    return  
            else:
                # event.status == "C"
                messages.error(request, 'Evento concluido')
        else:
            messages.error(request, 'Relación ya marcada como ganadora')


def set_status_refused(modeladmin, request, queryset):
    queryset.update(status='R')

def set_status_finished(modeladmin, request, queryset):
    for q in queryset:
        if q.status == "W":
            q.status = 'F'
            q.save()
            # var_token = q. notificationToken
            # send_push_message(token=var_token, message='Ganaste' )
            messages.success(request, 'Se marcó como pagada')
        else:
            messages.error(request, 'Relación no ganadora')


class postrelationsadmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('event', 'instaaccount', 'status', 'createTime')
    actions = [set_status_winner, set_status_refused, set_status_finished]


class InstaStoryPublicationAdmin(admin.ModelAdmin):
    list_filter = ('person',)
    list_display = ('person', )

admin.site.register(eventpost)
admin.site.register(postrelations, postrelationsadmin)
admin.site.register(InstaStoryPublication, InstaStoryPublicationAdmin)
