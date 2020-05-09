from django.contrib import admin
from django.urls import include, path

from eventos.views import blog_post_create_view

from .views import (contacto_view, home_view, quienes_somos_view,
                    user_list_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('contacto', contacto_view),
    path('quienes-somos', quienes_somos_view),
    path('eventos/', include('eventos.urls')),
    path('Create-Event', blog_post_create_view),
    path('Users', user_list_view),

    # ACCOUNTS VIEWS
    path('accounts/', include('accounts.urls')),

    # REST FRAMEWORK URLS
    path('api/eventos/', include('eventos.api.urls')),
    path('api/accounts/', include('accounts.api.urls'))
]
