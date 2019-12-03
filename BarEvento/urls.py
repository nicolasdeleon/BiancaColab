
from django.contrib import admin
from django.urls import path
from .views import (
    BarEvents_alldetail_view,
    BarEvento_event_view,
    blog_post_update_view,
    blog_post_delete_view,
)

urlpatterns = [
    path('', BarEvents_alldetail_view),
    path('<slug:slug>',BarEvento_event_view),
    path('edit/<slug:slug>',blog_post_update_view),
    path('delete/<slug:slug>',blog_post_delete_view),
]
