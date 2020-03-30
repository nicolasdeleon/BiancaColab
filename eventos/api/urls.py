from django.urls import path

from eventos.api.views import (
    api_detail_eventpost_view,
    api_addUser_eventpost_view,
    api_eventrel_state,
    api_won_events_view,    
    api_PostRelations_view,
    api_all_events_view,
    api_fin_event_view,
    api_create_eventpost,
)

urlpatterns = [
    path('adduser',api_addUser_eventpost_view,name='adduser'), #importante que vaya primero!
    path('<slug:slug>',api_detail_eventpost_view,name='detail'),
    #path('wonEvent/',api_won_event_view,name='wonEvent'),
    path('wonEvents/<slug:slug>',api_won_events_view,name='wonEvents'),
    path('eventrel_state/',api_eventrel_state,name='eventrel_state'),
    path('post_relations/',api_PostRelations_view.as_view(),name="post_relations"),
    path('all_events/',api_all_events_view.as_view(),name="all_events"),
    path('create_event/', api_create_eventpost, name="create_events"),
    path('finEvent/',api_fin_event_view,name='finEvent'), 
    ]