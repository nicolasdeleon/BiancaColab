""" accounts urls """
from django.urls import path
from .views import (
    activation_view,
)

urlpatterns = [
    path('activate/<activation_key>/', activation_view),
]
