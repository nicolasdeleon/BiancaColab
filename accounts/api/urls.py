
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from accounts.api.views import (
    api_registration_view,
    ObtainAuthTokenView,
	account_properties_view,
	update_account_view,
    ChangePasswordView,
    send_feedback_view,
    reset_password,
    reset_password_confirm,
)

urlpatterns = [
    path('register',api_registration_view,name= 'register'),
    path('login',ObtainAuthTokenView.as_view(),name= 'login'),
	path('properties', account_properties_view, name="properties"),
	path('properties/update', update_account_view, name="update"),
    path('change_password', ChangePasswordView.as_view(), name="change_password"),
    path('feedback',send_feedback_view,name="feedback"),
    path('reset_password/', reset_password, name = 'reset_password'),
    path('reset_password/confirm/', reset_password_confirm.as_view(), name = 'reset_password_confirm'),
#    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]