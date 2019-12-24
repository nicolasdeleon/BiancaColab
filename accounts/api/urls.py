
from django.contrib import admin
from django.urls import path
from accounts.api.views import (
    api_registration_view,
    ObtainAuthTokenView,
	account_properties_view,
	update_account_view,
    ChangePasswordView,
    send_feedback_view,
)
#Probando algo de git

urlpatterns = [
    path('register',api_registration_view,name= 'register'),
    path('login',ObtainAuthTokenView.as_view(),name= 'login'),
	path('properties', account_properties_view, name="properties"),
	path('properties/update', update_account_view, name="update"),
    path('change_password', ChangePasswordView.as_view(), name="change_password"),
    path('feedback',send_feedback_view,name="feedback"),
]

#Probando un segundo commit para ver como es que se anidan en mi branch 
#Y consecuentemente en mi pullrequest para ser monitoreado por mis compañeros de trabajo