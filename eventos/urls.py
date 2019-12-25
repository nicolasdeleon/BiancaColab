
from django.contrib import admin
from django.urls import path
from .views import (
    eventpost_alldetail_view,
    eventpost_event_view,
    blog_post_update_view,
    blog_post_delete_view,
)

urlpatterns = [
    path('', eventpost_alldetail_view),
    path('<slug:slug>',eventpost_event_view),
    path('edit/<slug:slug>',blog_post_update_view),
    path('delete/<slug:slug>',blog_post_delete_view),
]
