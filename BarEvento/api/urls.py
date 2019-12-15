from django.contrib import admin
from django.urls import path
from BarEvento.api.views import (
    api_detail_BarPost_view,
    api_addUser_BarPost_view,
    api_won_event_view,
    api_won_events_view,
    api_PostRelations_view,
)

urlpatterns = [
    path('adduser',api_addUser_BarPost_view,name='adduser'), #importante que vaya primero!
    path('<slug:slug>',api_detail_BarPost_view,name='detail'),
    path('wonEvent/',api_won_event_view,name='wonEvent'),
    #path('wonEvents/<slug:slug>',api_won_events_view,name='wonEvents'),
    path('wonEvents/',api_won_events_view,name='wonEvents'),
    path('post_relations/',api_PostRelations_view.as_view(),name="post_relations"),
]

