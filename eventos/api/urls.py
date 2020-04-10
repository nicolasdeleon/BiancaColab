from django.urls import path

from eventos.api.views import (
    api_detail_Event_view,
    api_addUser_Event_view,
    api_eventrel_state,
    api_won_events_view,    
    api_Post_view,
    api_all_events_view,
    api_fin_event_view,
    api_create_Event,
)

urlpatterns = [
    path('adduser',api_addUser_Event_view,name='adduser'), #importante que vaya primero!
    path('<slug:slug>',api_detail_Event_view,name='detail'),
    #path('wonEvent/',api_won_event_view,name='wonEvent'),
    path('wonEvents/<slug:slug>',api_won_events_view,name='wonEvents'),
    path('eventrel_state/',api_eventrel_state,name='eventrel_state'),
    path('post_relations/',api_Post_view.as_view(),name="posts"),
    path('all_events/',api_all_events_view.as_view(),name="all_events"),
    path('create_event/', api_create_Event, name="create_events"),
    path('finalize_event/',api_fin_event_view,name='finalize_event'), 
    ]