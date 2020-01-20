
from django.contrib import admin
from django.urls import path
from .views import (
    email_test_view,
)

urlpatterns = [
    path('', email_test_view),
]
